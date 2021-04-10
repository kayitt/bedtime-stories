export class TimeUtils {
  formatUtcTime(date: Date): string {
    const result = date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
      timeZone: "UTC",
    });

    return result;
  }

  formatLocalTime(date: Date): string {
    const result = date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
      timeZone: "Europe/Berlin",
    });

    return result;
  }
}
