export class TeaConsumer {
  consume(cups: number): string {
    if (cups == 0) {
      return "You have not drank any tea.";
    } else if (cups == 1) {
      return "You have drank a tea.";
    }

    return `You have consumed ${cups} cups of tea.`;
  }
}
