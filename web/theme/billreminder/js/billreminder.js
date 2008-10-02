// JavaScript Document

$(document).ready(function(){
    $("#about").click(function(){
        $(".widearea").animate({
            marginLeft: "0px"
        }, 500);
        return false;
    });
    $("#download").click(function(){
        $(".widearea").animate({
            marginLeft: "-960px"
        }, 500);
        return false;
    });
    $("#development").click(function(){
        $(".widearea").animate({
            marginLeft: "-1920px"
        }, 500);
        return false;
    });
    $("#translate").click(function(){
        $(".widearea").animate({
            marginLeft: "-2880px"
        }, 500);
        return false;
    });
});
