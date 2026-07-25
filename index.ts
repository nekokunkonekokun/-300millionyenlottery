export interface Ticket {
  id: string;
  numbers: number[];
}

export interface DrawResult {
  winningNumbers: number[];
  jackpotWon: boolean;
  prizeAmount: number; // 円
}

export class Lottery300MillionYen {
  private readonly JACKPOT_PRIZE = 300_000_000; // 3億円
  private readonly CONSOLATION_PRIZE = 10_000;   // 1万円（組違い・下桁一致など）
  private readonly NUMBER_COUNT = 6;
  private readonly MAX_NUMBER = 43;

  /**
   * 宝くじ券を発行（購入）する
   */
  public buyTicket(): Ticket {
    const numbers: number[] = [];
    while (numbers.length < this.NUMBER_COUNT) {
      const num = Math.floor(Math.random() * this.MAX_NUMBER) + 1;
      if (!numbers.includes(num)) {
        numbers.push(num);
      }
    }
    numbers.sort((a, b) => a - b);

    return {
      id: Math.random().toString(36).substring(2, 9).toUpperCase(),
      numbers,
    };
  }

  /**
   * 抽せんを行い、1等3億円の当選判定をする
   */
  public draw(userTicket: Ticket): DrawResult {
    // 当せん番号の生成
    const winningNumbers = this.buyTicket().numbers;

    // 一致する数字の数をカウント
    const matches = userTicket.numbers.filter((num) =>
      winningNumbers.includes(num)
    ).length;

    // 判定ロジック
    let prizeAmount = 0;
    let jackpotWon = false;

    if (matches === this.NUMBER_COUNT) {
      prizeAmount = this.JACKPOT_PRIZE;
      jackpotWon = true;
    } else if (matches >= 3) {
      prizeAmount = this.CONSOLATION_PRIZE;
    }

    return {
      winningNumbers,
      jackpotWon,
      prizeAmount,
    };
  }
}

