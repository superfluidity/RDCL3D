/*
   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an  BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

if (typeof dreamer === 'undefined') {
    var dreamer = {};
}

dreamer.Event = (function (global) {
    'use strict';

    function Event () {
        this._listeners = {};     
    }

    Event.prototype.addL = function (type, listener) {
        if (typeof this._listeners[type] == "undefined"){
            this._listeners[type] = [];
        }
        this._listeners[type].push(listener);
    };

    Event.prototype.fire = function (event, args) {
        if (typeof event == "string"){
            event = { type: event };
        }
        if (!event.target){
            event.target = this;
        }

        if (!event.type){  //falsy
            throw new Error("Event object missing 'type' property.");
        }

        if (this._listeners[event.type] instanceof Array){
            var listeners = this._listeners[event.type];
            for (var i=0, len=listeners.length; i < len; i++){
                listeners[i].call(this, event, args);
            }
        }
    };

    Event.prototype.addListener = function (type, listener) {
        if (this._listeners[type] instanceof Array){
            var listeners = this._listeners[type];
            for (var i=0, len=listeners.length; i < len; i++){
                if (listeners[i] === listener){
                    listeners.splice(i, 1);
                    break;
                }
            }
        }

    };

    return Event;
}());

if (typeof module === 'object') {
    module.exports = dreamer.Event;
}
