function updateDeploymentInfo(args){
    console.log('updateDeploymentInfo')
    getDeploymentInfo({'id': args.id}, function(result){
        console.log(JSON.stringify(result));
    }, function(e){
        console.log("getDeploymentInfo Error", e);
    })
}

function getDeploymentInfo(args, success, error){
    $.ajax({
            url: "/deployments/"+args.id,
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error(result);
            }
        });
}

function getDeploymentNodeConsole(args, success, error){
    $.ajax({
            url: "monitoring/node/"+args.nodeId+"/shell",
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            success: function(result) {
                if (success)
                    success(result);
            },
            error: function(result) {
                if (error)
                    error(result);
            }
        });
}