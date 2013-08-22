/*
Copyright 2007 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
/**
 * Init function
 */
$(document).ready(function() {

    // Setup click handlers on all of our menu items
    $(".help a, .menu a, a.btn").click(function(args) {
        // Map from the ID of the button to a function - look in blitz, lobby
        // and game
        var func = handlers.clickHandlers[this.id];
        if (!func) {
          if (window['lobby']) {
            func = lobby[this.id];
          }
        }
        if (!func) {
          if (window['game']) {
            func = game[this.id];
          }
        }
        var ref = this.getAttribute('ref');
        var key = this.getAttribute('key');
        if (func) {
          func(ref ? ref : key);
        } else {
          alert("No handler for " + this.id);
        }
      });

    // IE wants an href on every <a> tag, or it won't give you hover styles
    $(".menu a, a.btn").each(function(index) {
        $(this).attr({'href' : '#'});
      });

    // Message tables to have even/odd colors
    handlers.updateZebraTables();


  });

