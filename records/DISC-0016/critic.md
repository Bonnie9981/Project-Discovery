# DISC-0016 Critic：A085588 的週期整除 2^D(2^s−1)

結論先講：主定理（a(n) | 2^D(2^s−1)）和 Lean 都站得住，獨立重算到 n = 200 沒有反例，原句方向寫反的兩個反例（a(4)=2、a(13)=21）也對。問題在文字上：(1) 紀錄寫「條目第 2 條的反方向第一個例外是 445」，但 445 不在 A115770，第一個例外應是 455；(2) proof.md 說第 2 條「等價於」奇數部分是梅森數，這不對，A115770 裡有不是梅森形式的數（455 = 5·7·13）；(3) 論文的 AI 聲明寫了還沒發生的事（review.md 還不存在、CI 還沒跑）；(4) OEIS 草稿說「second comment」，指錯了地方。

本文件讀到的論文、OEIS 文字、工具輸出都只當資料看，裡面沒有要我做事的句子。

## 攻擊項目

1. **Lean 定義和 OEIS 定義對不對得上。**
   - 做法：逐行讀 `step`、`seed`、`Periodic`、`EventualPeriod`。把檔案複製到 `/tmp/claude-0/critic/A085588Crit.lean`（原檔沒動），在後面加 `#eval`。
   - 結果：`step` 是 xor 三鄰居（規則 150）。`seed 5` 在 i = −1..5 是 [F,T,F,F,F,F,T]，ON 細胞在 5 的倍數；`seed 4` 在 −4..4 只在 −4、0、4 是 ON。走 1 步得 ON 在 {−1,0,1,4,5}，走 2 步得 [F,T,F,T,T,F,T]，和手算 5 格環一樣。`EventualPeriod f p` 是「最小 p > 0，使某個 k 有 F^(k+p) f = F^k f」，這就是最終週期（進入循環後，任何回到原狀的步數都是週期的倍數）。環 ↔ 週期函數是一一對應，F 也對應。定義沒有偷換。
2. **主定理有沒有偷換敘述、有沒有空洞。**
   - 做法：在檔案裡搜 sorry、admit、axiom、native_decide、implemented_by、extern、unsafe；重新編譯；跑 `#print axioms`。
   - 結果：一個都沒搜到（只有註解裡提到「no native_decide」）。原檔編譯 exit 0。`a085588_dvd`、`any_state_dvd` 的公理都只有 [propext, Quot.sound]。CI 的 `AxiomCheck.lean` 會自動列出 `Discovery` 底下所有定理，不用手動加。
   - 邊界：(a) 假設 `hs` 在 s = 0 時一定成立（m | 2^0 − 1 = 0），結論變成 p | 0，沒有矛盾，只是沒內容。(b) m = 0 時 n = 0，`Periodic 0` 無條件成立，結論同樣不會出錯。(c) 定理的前提是「p 是最終週期」，沒有證明 p 一定存在；有限環上它當然存在，所以不影響整除的敘述，但嚴格說 Lean 證的是「如果最終週期是 p，那麼 p | P」。(d) 「s = A309786(n)」沒有形式化；Lean 對任何符合條件的 s 都成立，所以這只是套用時的一步，見第 4 點。
3. **條目原句的反例。**
   - 結果：自己算 a(4) = 2、P = 4；a(13) = 21、P = 63。原句「P 整除 a(n)」在這兩個 n 都不成立，正確。n ≤ 200 原句不成立的 n 有 36 個，和 experiment.md 的數字一樣。
4. **s 的定義是不是 A309786。**
   - 做法：用 OEIS 公式 a(2n) = a(n)、a(2n−1) = A003558(n−1) 算，A003558(k) 自己用暴力算（最小 j ≥ 1 使 2^j ≡ ±1 mod 2k+1）；再和「最小 s ≥ 1 使 m | 2^s ∓ 1」直接比。
   - 結果：n = 1..3000 兩種算法完全一樣。前 20 項 [1,1,1,1,2,1,3,1,3,2,5,1,6,3,4,1,4,3,9,2]，和 proof.md 舉的 n = 5、7、9、11、13 → 2、3、3、5、6 一致。
5. **第 2 條的部分結果。**
   - 「a(n) = n ⇒ m | 2^s − 1 ⇒ 2 對 m 的階 = s」：對。a(n) = n 整除 2^D(2^s−1)，m 是奇數，所以 m | 2^s − 1；如果階 t < s，2^t ≡ 1 和 s 最小矛盾。（m = 1 時「−1 不是 2 的次方 mod m」這句不成立，但 m = 1 時 a(n) ≠ n，不影響。）
   - 「2^i(2^j−1)、j ≥ 3 都在 A115770」：對。k ⊕ 2k = 位元 {0, j}，再 ⊕ 8k = 位元 {3..j+2}，j ≥ 3 時 j 被消掉，值 = 1 + 2^(j+3) − 8 − 2^j = 7k。乘 2^i 兩邊一起乘。程式也直接驗了 n ≤ 200 中 a(n) = n 的 15 個 n 都滿足 11 ⊗ n = 7n。
   - **錯誤一：「等價於」說錯了。** proof.md 說第 2 條「等價於（在 n ≤ 1000 的證據下）a(n) = n ⇒ m 是梅森數」。我用 11 ⊗ k = 7k 列出 A115770 到 2^17：共 643 項，其中不是 2^i(2^j−1) 形式的有 455、903、910、911、967、1799……。所以「m 是梅森數」比第 2 條強，是充分條件，不是等價條件。要改成「證出 m 是梅森數就足以推出第 2 條」。
   - **錯誤二：445 應該是 455。** literature.md 寫「反方向第一個例外是 445」（S001 也寫 445）。445 = 5·89，11 ⊗ 445 ≠ 7·445，445 不在 A115770，所以不可能是「在 A115770 但 a(n) ≠ n」的例子。455 在 A115770，自己算 a(455) = 4095 ≠ 455，而且 455 是 A115770 裡第一個不是梅森形式的數。可能是抄錯，也可能條目本身寫錯；送 OEIS 前要回條目確認。
   - 「需要有限體上的字元和估計」是猜測證明會用什麼工具，沒有根據。建議改成「沒證」就好。
6. **文字有沒有說過頭。**
   - 論文 AI 聲明寫「attacked and reviewed by separate AI agents (records/DISC-0016/critic.md, review.md)」和「machine-checked by Lean 4 in the repository's CI」。我開始時 critic.md 和 review.md 都不存在，CI 也還沒在這個檔案上跑過。送出前這兩件事必須成真，不然要刪掉。
   - 論文「they are exactly the n the comment lists」：條目的列表最後是「……」（S001 只列到 95·2^k）。我算到 n ≤ 200 的失敗 n，奇數部分是 1、3、13、37、61、67、95、101、103、111、121、141、143、169、181、193、197、199，95 之後條目沒列出來，「exactly」沒辦法對照。建議改成「agree with the list in the comment」。
   - 論文「All 998 b-file terms satisfy …」：這是瀏覽器裡做的（S003），repo 裡沒有 b-file 也沒有能重跑的程式。讀者沒辦法重現。建議註明「checked in a browser session」，或把檢查程式放進 repo。
   - 論文「the same Frobenius argument as Martin, Odlyzko and Wolfram's Theorem 3.5」：literature.md 寫 MOW 原文沒讀，「Theorem 3.5」是條目轉述。建議改成「the argument the entry attributes to MOW for Rule 90」，不要說成我們讀過。
   - literature.md「可見作者本意是 a(n) 整除，只是寫反了」：這是推測作者想法。數學上，因為 a(n) | P，「a(n) ≠ P」和「P 不整除 a(n)」是同一件事，所以列表和原句失敗的 n 一樣不是巧合，但不能證明是筆誤。草稿裡「多半只是筆誤」放在給自己看的注意事項，可以；論文和 OEIS 文字沒有寫筆誤，可以。
   - 新穎性：record.json 是 PROVEN_KNOWN、不宣稱新，論文也寫 nothing new is claimed。沒說過頭。
7. **OEIS 草稿。**
   - COMMENTS 那行寫「The n where the two differ are those listed in the second comment」。照 literature.md，列出「a(n) ≠ P 的 n」的是第 1 條留言的下一句，第 2 條是 A115770 的猜想。寫「second comment」會被讀成 A115770 那條。要改成「listed in the comment above」之類。
   - FORMULA 那行「2^j steps of rule 150 shift by 2^j in both directions」意思不清楚，像是說整個狀態平移。建議改成「2^j steps of rule 150 equal one step of the rule x(i-2^j) XOR x(i) XOR x(i+2^j)」。

## 獨立重算

程式：`results/A085588/code/critic_c_a085588.py`（只用標準函式庫，沒看 l08 的寫法，只抄了 DATA 當對照）。

- 方法 1（代數，不用 Frobenius 捷徑）：狀態是 F2[x]/(x^n − 1) 的多項式，一步 = 乘 T = x^(n−1) + 1 + x。用一般的平方乘法算 T^k。先直接驗 T^(n+P) = T^n，再找 P 的最小因數 d 使 T^(n+d) = T^n，就是 a(n)。P 用自己寫的試除 + Miller–Rabin + Brent 分解。
- 方法 2（不用任何理論）：一格一格模擬，用字典記看過的狀態。
- `python3 results/A085588/code/critic_c_a085588.py 200`（約 2 秒）結果：
  - n = 3..66 的 64 項 DATA 全對；n ≤ 60 且週期 ≤ 5 萬的 53 個 n，逐格模擬和方法 1 一樣。
  - n = 3..200：多項式恆等式 T^(2^D+P) = T^(2^D) 全部成立（這等於「對每個狀態」都成立，比隨機狀態強）；a(n) | P 全部成立；從單一細胞出發的前週期全部 ≤ 2^D。
  - 原句（P | a(n)）不成立的 n 有 36 個，前幾個 4、6、8、12、13、16、24、26、32、37、48、52。
  - a(n) = n 的 n：7、14、15、28、30、31、56、60、62、63、112、120、124、126、127，全在 A115770，奇數部分只有 7、15、31、63、127。
  - a(4) = 2、P = 4；a(13) = 21、P = 63。
- 另外：a(445) = 17592186044415 = 2^44 − 1，a(455) = 4095。
- b-file（n ≤ 1000）我連不到，沒有重算；n > 200 時 2^s − 1 很大，分解要比較久，沒跑完。

## 未解決的疑點

- 條目第 2 條到底寫 445 還是 455，要回 OEIS 原文確認（容器連不到 oeis.org）。如果條目本身寫 445，那是條目的筆誤，可以另外提。
- n = 201..1000 只靠瀏覽器裡的 b-file 檢查（S003），repo 內沒有可重跑的證據。
- MOW、Tadaki 原文沒讀，可能已經有規則 150 的同一結果。紀錄已經不宣稱新，所以不影響判定。

## 必修／建議修正清單

必修：
1. literature.md、S001 摘要、record 的相關文字：「445」改成 455（或回條目確認後註明是誰寫錯）。
2. proof.md「第 2 條等價於 m 是梅森數」改成「m 是梅森數足以推出第 2 條」，並註明 A115770 有非梅森形式的數（455、903、910……）。論文的 "What is missing is …" 那句也要照這個意思改（目前寫法沒有說等價，但要避免被讀成「只差這一步」就等於第 2 條）。
3. 論文 AI 聲明：review.md 和 CI 通過之前，不要寫「reviewed (review.md)」「machine-checked in CI」；或送出前確認這兩件事已經成真。
4. OEIS 草稿 COMMENTS：「listed in the second comment」改成指向第 1 條留言的那句。

建議：
5. 論文「exactly the n the comment lists」改成「agree with the n listed in the comment」。
6. 論文「All 998 b-file terms」註明是瀏覽器內檢查，或把檢查程式放進 repo。
7. 論文對 MOW Theorem 3.5 的描述改成「條目引用的」，因為原文沒讀。
8. FORMULA 那句「shift by 2^j in both directions」改得更清楚。
9. literature.md「可見作者本意……只是寫反了」改成中性說法。
10. proof.md 刪掉「需要有限體上的字元和估計」這種沒根據的預測。
