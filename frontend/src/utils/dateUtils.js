function formatTime(input) {
  let date;

  if (typeof input === "string") {
    date = new Date(input);
    if (isNaN(date)) {
      throw new Error("Invalid date string");
    }
  } else if (input instanceof Date) {
    date = input;
  } else {
    throw new Error("Input must be a string or a Date object");
  }

  let hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12;
  hours = hours ? hours : 12;
  const minutesFormatted = minutes < 10 ? "0" + minutes : minutes;
  return `${hours}:${minutesFormatted} ${ampm}`;
}
export { formatTime };
