const helpers = {};

const days = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday"
];

const months = [
  "January",
  "Februrary",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

helpers.parseDate = (startDate, startTime, endDate, endTime) => {
  const startDateObj = new Date(startDate);
  const endDateObj = new Date(endDate);

  return `${days[startDateObj.getDay()]} ${startDateObj.getDate()} ${
    months[startDateObj.getMonth()]
  } ${startTime} - ${days[endDateObj.getDay()]} ${endDateObj.getDate()} ${
    months[endDateObj.getMonth()]
  } ${endTime}`;
};

export default helpers;
