export class TimeUtils {
  formatTime(date: Date): string {
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const amPm = hours >= 12 ? "PM" : "AM";

    hours = hours % 12;
    hours = hours ? hours : 12;
    const minutesString = minutes < 10 ? "0" + minutes : minutes;

    return `${hours}:${minutesString} ${amPm}`;
  }
}
