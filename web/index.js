//d -> JSON object from json.js

//would get none because it hasn't loaded yet. use window.onload to wait until the page loads
window.onload = function(){
  addButtons("insertbtns", d, 1);
}

function addButtons(ID, d, count){
  /* Adds buttons to a dropdown element for each key in the dictionary `d`

  :param ID: The .id of the dropdown element. Append the newly created buttons to this element.
  :type ID: string
  :param d: a dictionary. keys are the relative category, and the values are the relative sub-categories.
  :type d: object
  :param count: the dropdown element number where the buttons are placed.
  :type count: number
  :rtype: undefined
  */
  console.log("id: ", ID);
  console.log("d: ", d);

  var dropdown = document.getElementById(ID);
  dropdown.innerHTML = ""; //empty list

  for(var key in d){
    //create a single button with .class, .type, .innerHTML, and .onclick attributes

    var btn = document.createElement("button");
    btn.className = "dropdown-item";
    btn.type = "button";
    btn.innerHTML = key;

    console.log("typeof key", typeof key);
    /*onclick function*/
    if(d[key][0] === undefined){
      //a dictionary (nested, more to come)
      btn.onclick = deepOnClick(d[key], key, count)
    } else{
      //a list (end of dropdowns)
      btn.onclick = shallowOnClick((count + 1) + "-insertbtns", d[key], count, key);
    }
    dropdown.appendChild(btn);
  }
}

function deepOnClick(d, title, count){ 
  /*Returns the .onclick attribute for elements that require further selection.*/
  return function(){
    console.log("onclick nested");
    console.log("replace: ", count + "-btnholder");
    document.getElementById(count + "-btnholder").innerHTML = title; // add name to current dropdown

    //remove & make
    hideDropdown(count + 1);
    showDropdown(count + 1);

    addButtons((count+1) + "-insertbtns", d, count + 1); //add buttons to the next dropdown
  }
}

function shallowOnClick(ID, keys, count, title){
  /*Returns the .onclick attribute for the 2nd-to-last-category dropdown button. Iterates over arrays, versus a dictionary. 
  :param ID:
  :type ID:
  :param keys:
  :type keys:
  :param count:
  :type count:
  :param title:
  :count title:
  :returns: A function used as the .onclick attribute for the dropdown button.
  :rtype: function

  Last time filling in dropdown.
  Iterates over a list*/

  return function(){

    document.getElementById(count + "-btnholder").innerHTML = title; // add name to current dropdown

    //hide and show
    hideDropdown(count + 1);
    showDropdown(count + 1);

    var dropdown = document.getElementById(ID);
    dropdown.innerHTML = ""; //empty list

    for(var i = 0; i < keys.length; i++){
      var btn = document.createElement("button");
      btn.className = "dropdown-item";
      btn.type = "button";
      btn.innerHTML = keys[i];

      /*onclick function*/
      btn.onclick = function(){
        document.getElementById((count + 1) + "-btnholder").innerHTML = this.innerHTML;
        console.log(this.innerHTML);
        accessPhotos(this.innerHTML);
      };

      dropdown.appendChild(btn);
    }
  }
}

function hideDropdown(count){
  /*Adds hiding styles to the #-drop element, where # is count <= # < 4.*/
  for(var i = count; i < 4; i++){
    var element = document.getElementById(i + "-drop");

    if(element !== undefined && element !== null){
      element.getElementsByTagName("button")[0].innerHTML = "Sub-category";
      element.style = "display:none;";
    }
  }
}

function showDropdown(count){
  /*Removes any hiding styles from the #-drop element, where # is count.*/
  console.log("showDropdown: ", count);
  var element = document.getElementById(count + "-drop");

  if(element !== undefined && element !== null){
    element.style = "";
  }
} 

function accessPhotos(queryName){
  /*Sets the .src attribute of the image tag under 'View Graphs' to the directory of the image corresponding to 'queryName.'
  :type queryName: string
  */
  var directory = "../data_files/PNG/" + queryName.replace(/ /g, "_") + "_combo.png";
  document.getElementById("photo").src = directory;
}