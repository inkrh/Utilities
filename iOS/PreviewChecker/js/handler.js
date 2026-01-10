var content = $('.device-content');
var hintText = $('.contenttext');
var hintTextl = $('.contenttextlandscape');
var xsmax = $('#xsmax');
var eightplus = $('#8p');
var ipadpro = $('#ipadpro');
var xsmaxl = $('#xsmaxl');
var eightplusl = $('#8pl');
var ipadprol = $('#ipadprol');
var deviceSelector = $('#contentSwitch');
var orientation = ""

function allowDrop(ev) {
  ev.preventDefault();
}

function drop(ev) {
  ev.preventDefault();
  var files = ev.target.files || ev.dataTransfer.files;
  var reader = new FileReader();
  reader.onload = function (e) {
    hintText.hide();
    hintTextl.hide();
    content.css('background-image', 'url(data:' + e.target.result + ')');
  }

  reader.readAsDataURL(files[0]);
}

function switchContent(v) {
  xsmax.css('display', 'none');
  eightplus.css('display', 'none');
  ipadpro.css('display', 'none');
  xsmaxl.css('display', 'none');
  eightplusl.css('display', 'none');
  ipadprol.css('display', 'none');
  $('#' + v + orientation).css('display', 'block');
}

function switchOrientation(v) {
  orientation = v;
  switchContent(deviceSelector.val());
}

function landing() {
  xsmax.css('display', 'block');
  eightplus.css('display', 'none');
  ipadpro.css('display', 'none');
  xsmaxl.css('display', 'none');
  eightplusl.css('display', 'none');
  ipadprol.css('display', 'none');
}

window.onload = landing();