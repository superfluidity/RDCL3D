#!/bin/bash

# requires jq

#######################
################## VARIABLES && CONSTANTS
#######################

NSDFILE="nsd.json"
FLAVORUUID="5a258552-0a51-11e7-a086-0cc47a7794be"
# openvim client
OPENVIM="/home/openvim/openvim-one/openvim/openvim" 
CLICKINJECTOR="/home/openvim/rdcl3dopenvim/configinjector"
STAMINALCLICKOSIMAGE="/home/openvim/rdcl3dopenvim/clickos_x86_64_staminal"

# directory to store yamls
YAMLDIR="$(pwd)/yamls"

# store the UUIDs in these arrays
declare -A UUID_images
declare -A UUID_networks

# map vnf to vdu
# ASSUMPTION: a VNF has only one VDU
declare -A VNF2VDU

# map virtualLinkProfileId to virtualLinkId
declare -A VLPID2VLID

#######################
################## FUNCTIONS
#######################

transformlist() {
    # this function transforms a json list into a (more bash friendly) space separated list
    sed 's/[]"\[]//g' | sed 's/,/\ /g'
}

generateimageyaml() {
    # generates a yaml for an openvim clickos image
    cat - <<EOF 
image:
    name:         clickos-${1}
    description:  click-os ${1} image
    path:         /var/lib/libvirt/images/clickos_${1}
    metadata:     # Optional extra metadata of the image. All fields are optional
        use_incremental: "no"          # "yes" by default, "no" Deployed using a incremental qcow2 image
EOF
}

generatenetworkyaml() {
    # generates a yaml for an openvim network
    cat - <<EOF 
network:
    name:               net-${1}
    type:               bridge_data
    provider:           OVS:default
    enable_dhcp:        false
    shared:             false
EOF
}

generatemacaddress() {
    # generate a random MAC address
    printf '00:15:17:%02x:%02x:%02x' \
        $(echo $RANDOM | sed 's/.*\(..\)$/\1/') \
        $(echo $RANDOM | sed 's/.*\(..\)$/\1/') \
        $(echo $RANDOM | sed 's/.*\(..\)$/\1/')
}

generatevmyaml() {
    # generates a yaml for an openvim vm
    name=$1
    imageuuid=$2
    shift 2
    netuuids="$@"
    cat - <<EOF 
server:
  name: vm-clickos-${name}
  description: ClickOS vm 
  imageRef: '${imageuuid}'
  flavorRef: '${FLAVORUUID}'
  start:    "yes"
  hypervisor: "xen-unik"
  osImageType: "clickos"
  networks:
EOF
    i=0
for netuuid in $netuuids; do
    echo "  - name: vif${i}"
    echo "    uuid: ${netuuid}"
    echo "    mac_address: $(generatemacaddress)"
    i=$(($i + 1))
done

}


#######################
################## MAIN
#######################

mkdir -p "$YAMLDIR"

# 1. create and onboard the ClickOS images

# take the VNF IDs from the NSD
vnfids="$(jq -r -c '.["vnfdId"]' ${NSDFILE} | transformlist)"

for vnfid in $vnfids; do
    echo "vnfid: $vnfid"

    if [ ! -e "${vnfid}.json" ]; then
        echo "${vnfid}.json file not found. skipping"
        continue
    fi

    # search for the click vdu in the VNF descriptor
    # search for all the vduIds of the VDUs that have vduNestedDescType == "click"
    vduids=$(jq '.["vdu"][] | select(.vduNestedDescType == "click") | .["vduId"]' "${vnfid}.json" | transformlist)
    # ASSUMPTION: we have at most one vduid per vnfid
    vduid=$(echo $vduids | awk '{print $1}')

    echo "vduid: $vduid"

    if [ ! -e "${vduid}.click" ]; then
        echo "${vduid}.click file not found. skipping"
        continue
    fi

    # ASSUMPTION: ids (vduid, vlid) are strings without spaces
    # keep track of the correspondance between VNF and VDU
    VNF2VDU[${vnfid}]=${vduid}

    # create a new image corresponding to the click configuration
    cp "$STAMINALCLICKOSIMAGE" "${YAMLDIR}/clickos_${vduid}"
    $CLICKINJECTOR "${vduid}.click" "${YAMLDIR}/clickos_${vduid}" 

    # copy the image to the server. The way to do this is not defined by openvim, so we use scp
    # ASSUMPTION: we are using scp to transfer images to openvim
    scp "${YAMLDIR}/clickos_${vduid}" root@127.0.0.1:/var/lib/libvirt/images/

    # create the yaml for the image
    echo "generating yaml: image-clickos-${vduid}.yaml"
    generateimageyaml ${vduid} > ${YAMLDIR}/image-clickos-${vduid}.yaml
    # onboard the image and get its UUID
    UUID_images[${vduid}]=$($OPENVIM image-create ${YAMLDIR}/image-clickos-${vduid}.yaml | awk '{print $1}') 
    # TODO: check if onboarding was successful
    echo "UUID: " ${UUID_images[${vduid}]}

done


# 2. create the networks corresponding to the virtuallinks

vlids="$(jq -r -c '.["virtualLinkDesc"][] | .["virtualLinkDescId"]' ${NSDFILE} | transformlist)"

for vlid in $vlids; do
    echo "virtualLinkDescId: $vlid"
    # create the yaml for the network corresponding to the virtuallink
    echo "generating yaml: net-${vlid}.yaml"
    generatenetworkyaml ${vlid} > ${YAMLDIR}/net-${vlid}.yaml
    # onboard the network and get its UUID
    UUID_networks[${vlid}]=$($OPENVIM net-create ${YAMLDIR}/net-${vlid}.yaml | awk '{print $1}')

    # FIXME: openvim does not yet create the ovs bridge automatically, so here we create it manually
    uuid=${UUID_networks[${vlid}]}
    vlanid=$($OPENVIM net-list -vvv $uuid | grep 'provider:vlan' | awk '{print $2}')
    sudo ovs-vsctl --may-exist add-br ovim-${vlanid}
done


# 3. create the VNFs, using references to the created images and networks

# find the mapping between each virtualLinkProfileId and virtualLinkDescId 
# ASSUMPTION: we have only one nsDf in the NSD
# populate the VLPID2VLID array
eval "$(jq -r -c '.["nsDf"][0]["virtualLinkProfile"][] | [.["virtualLinkProfileId"], .["virtualLinkDescId"]]' $NSDFILE | transformlist | awk '{print "VLPID2VLID[\"" $1 "\"]=" $2 }')"

for vnfid in $vnfids; do
    echo "vnfid: $vnfid"

    vduid=${VNF2VDU[$vnfid]}

    echo "vduid: $vduid"
    if [ -z "$vduid" ]; then
        echo "skipping..."
        continue
    fi

    echo "image UUID: ${UUID_images[$vduid]}"
    
    # ordered array of network UUIDs
    unset NETUUIDS || true
    declare -a NETUUIDS

    # search for the connection points of this VNF in the nsd, and their associated virtualLinkProfileId, to find the UUIDs of the networks
    # ASSUMPTION: on a virtuallink there is at most one extCP per VNF (i.e. a VNF does not have two interfaces on the same network)
    for line in $(jq -r -c '.["nsDf"][0]["vnfProfile"][] | select(.vnfdId == "'${vnfid}'") | .["nsVirtualLinkConnectivity"][] | select(.["virtualLinkProfileId"] != null) | [.["cpdId"][0], .["virtualLinkProfileId"]]' $NSDFILE); do

        echo "line: " $line

        # iterate on the external connection points of this VNF
        cpdId=$(echo $line | transformlist  | awk '{print $1}')

        # each external connection point is connected to a virtuallink
        virtualLinkProfileId=$(echo $line | transformlist | awk '{print $2}')

        echo "vlid: $virtualLinkProfileId"

        # virtualLinkProfileId -> virtualLinkDescId
        vlid=${VLPID2VLID[$virtualLinkProfileId]}

        # virtualLinkDescId -> openvim UUID
        netUUID=${UUID_networks[$vlid]}

        # now search for the corresponding internalIfRef 
        # cpdId -> intVirtualLinkDesc
        intVirtualLinkDesc=$(jq -r -c '.["vnfExtCpd"][] | select(.["cpdId"] == "'${cpdId}'") | .["intVirtualLinkDesc"]' ${vnfid}.json | sed 's/"//')

        # intVirtualLinkDesc -> internalIfRef
        internalIfRef=$( jq -r -c '.["vdu"][0]["intCpd"][] | select(.["intVirtualLinkDesc"] == "'${intVirtualLinkDesc}'") | .["internalIfRef"]' ${vnfid}.json | sed 's/"//')

        # populate the NETUUIDS array 
        NETUUIDS[$internalIfRef]=$netUUID
    done
    
    # generate the YAML for this VNF
    generatevmyaml ${vnfid} ${UUID_images[$vduid]} ${NETUUIDS[@]} > ${YAMLDIR}/vm-clickos-${vnfid}.yaml
    # onboard
    $OPENVIM vm-create ${YAMLDIR}/vm-clickos-${vnfid}.yaml
done

