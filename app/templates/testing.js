'use strict';
const today = new Date();
var month = today.getMonth() + 1;
var year = today.getFullYear();


/*function getAmPm(){
    let dateTime = new Date();
    let hours = dateTime.getHours();
    let amPm = 'morning';
    if (hours >= 12)
    amPm = 'afternoon';
    $('#ampmSpan').html(amPm);
}

function getDateTime(){
    let dateTime = new Date();
    $('#datetimeSpan').html(dateTime.toLocaleString());
}*/

function handleCalendar(response){
    $('#calendar_info').html(response);
}
function handleDay(response){
    $('#day_panel').html(response);
}

let request = null;

function getCalinfo()
{
        // look at how you retrieve information
        let url = '/calender';

        if (request != null)
        request.abort();

        request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleCalendar
        }
        );
}

function get_events(day_id) {
    // $('#' + clicked_id).css("{background-color: red}")
    let day = 0;
    let month = 0;
    let year = 0;

    if (day_id == "today") {
      let today = new Date();
      day = String(today.getDate());
      month = String(today.getMonth() + 1);
      year = String(today.getFullYear());
    }
    else {
      day = String(clicked_id);
    }

    let url = "/caldayinfo?day=" + day + "&month=" + str(month) + "&year=" + str(year);

    if (ev_request != null) 
      ev_request.abort();

    ev_request = $.ajax(
        {
            type: 'GET',
            url: url,
            success: handleDay
        }
    );
  }
  function prev_month() {
      month = month - 1;
      if(month == 0) {
          month = 12;
          year = year -1;
      }
  };
  function next_month() {
      month = month + 1;
      if(month == 13) {
        month = 1;
        year += 1;

      }
  }


function setup() {
    getCalinfo();
    get_events("today");
}
document.querySelector(".prev").addListener("click", ()=>{
    prev_month();
    getCalinfo();
});
document.querySelector(".next").addListener("click", ()=> {
    next_month();
    getCalinfo();
});



    $('document').ready(setup);
