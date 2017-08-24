// swap tagline

$(document).ready(
       setInterval(function () {
           var text = "for your business";
           if ($("#taglineSwap").html() == '') {
               text = "for your business";
           } else if ($("#taglineSwap").html() == "for your business") {
               text = "for your customers";
           } else if ($("#taglineSwap").html() == "for your customers") {
               text = "for the future";
           }
           $("#taglineSwap").html(text);
       }, 5120));
