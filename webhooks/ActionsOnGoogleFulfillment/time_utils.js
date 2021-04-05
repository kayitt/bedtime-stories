exports.toSimpleTime = function(date) {
    return formatTime(date);
  };

  function formatTime(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var amPm = hours >= 12 ? 'PM' : 'AM';

    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' +  date.getMinutes() + ' ' + amPm;

    return  `${hours}:${minutes} ${amPm}`;
  }