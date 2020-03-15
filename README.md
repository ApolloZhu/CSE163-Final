# Analysis on Factors Contributing to Animes’ Popularity

Final project for [CSE163: Intermediate Data Programming](https://cse-163.pages.cs.washington.edu/cse-163-20wi/website/project/overview.html) by

- [Hairong (Jason) Wu](https://github.com/YuudachiXMMY) (hwu9 at uw dot edu)
- [Zhiyu (Apollo) Zhu](https://github.com/ApolloZhu) (zhuzhiyu at uw dot edu)

## Research Questions & Results

1. **How favored anime genre change over time?** Comedy, Action, Shounen (youngster), Drama, and School are the consistently the most popular genres over the past 5 years for top animes. Supernatural become popular in recent years but audiences are starting to become less interested. Yuri (girls love) is a niche culture.
2. **What factors makes an anime popular?** Duration per episode, number of Episodes, and whether an anime Sources from manga are the most weighted influencers in predicting an anime’s score on MyAnimeList based on our trained `DecisionTreeRegressor`.

## Motivation and Background

Due to the prevailing [coronavirus](https://www.who.int/emergencies/diseases/novel-coronavirus-2019) and other possible future disasters, anime industry also becomes one of the majority of the industries that have been affected by these disasters. “The global issues of the COVID-19 coronavirus illness have had a big effect on the production”, explained by a staff from [*Re:ZERO - Starting Life in Another World*](http://re-zero-anime.jp/), an anime which has its premiere date delayed from April to July ([Hodgkins, 2020](https://www.animenewsnetwork.com/news/2020-03-09/re-zero-tv-anime-2nd-season-delayed-to-july/.157306)). Therefore, anime producers now need to make plans and concern which type of anime they need to produce in order to achieve a higher popularity, rating, and revenue. Therefore, we want to use all the statistics of previous animes to analysis factors that would lead an anime to succeed, such as its genres, premiered season, duration, etc. The result will allow anime producers to focus more on what most of the audience would prefer to watch, thus focusing producing more high quality animes under these features for higher popularity and revenue.

## Dataset

There are 3 datasets: [full](./full.csv), [sample](./sample.csv), and [future](./future.csv). To generate another dataset yourself, open the [build_dataset.py](./build_dataset.py) and follow the instructions at the bottom of the script. Currently, it’s set to produce the future dataset.

Full dataset contains anime information from earliest possible (spring 1961) to winter 2020 (current season). Some seasons (in the early years) might contain no anime because none was produced.

Sample dataset contains anime information from winter 2019 to winter 2020 (current season). Because this was generated at a different time than the full dataset, `Score`, `Members`, and `Favorites` column might have a different number as these metrics change over time.

Future dataset contains anime information for future seasons (as of now). The provided csv is for spring and summer 2020. This dataset differs from the other ones because its “Score” column (which is what we try to predict with our research question 2) is empty.

The following table shows a few rows of the dataset format. Starting with the “Action” column, each column represents one possible anime genre, where value 1 means the anime is of that genre and “missing data” means it’s not.

<script src="https://gist.github.com/ApolloZhu/75d84a941a23b1e4db73977b104e2524.js"></script>

## Methodology

### For Research Question 1

We will visualize the percentages of the genres of (up to) top 10 anime of all seasons vs time to demonstrate change in viewers’ taste and what’s the most recent popular genre. Many animes have several genres and each of those will be counted. For animes that span over several seasons, our analysis will only count it for the season in which it was premiered. The final visualization should be like a stacked area graph spanning over years and seasons instead of months within a year.

If a genre becomes thicker over years, then this means that this genre is more welcomed by audiences; otherwise, become less popular among most audiences.

### For Research Question 2

We will use `DecisionTreeRegressor` to train a model to predict the score for a future anime on My Anime List. We’ll use all the information stored in our dataset except column `ID`, `Year`, `Name`, `English`, `Japanese`, `Broadcast` (time), and the “label” to predict (`Score`, `Members`, and `Favorites`). We split 20% of our dataset as a test set and 80% as a train set. Then, we use the test set to test the mean squared error of our trained model. The accuracy of the trained model will be measure using its mean squared error on test dataset. If the error is reasonably low, such machine learning model can be used to predict a future anime’s popularity.

## Results

### Of Research Question 1

Because of our methodology includes all genres for all popular animes, the results are clustered with anime genres that might be popular in 1 season only but not any other. To filter out those that’s only a flash, we’ll filter what’s included the stacked area graphs for trend analysis using:

> **consistency requirement**: genre is only popular if it’s popular for at least 40% of the seasons analyzed. 

While 40% is an arbitrary choice, this should allow us to cache new trends that’s developing while filtering out majority of noises. When performing additional analysis based on our work, one could set it to 100% to find people's favorites of all time, or to 1 season to include all genres in the graph.

Genres in the legend of following two figures are the most popular genres in the last five years. The legend of the graph is sorted by total area of a genre, with the largest on the top (while stacked at the bottom in the graph).

This shows the change in distribution of genres of top **5** anime:

![popular genres for top 5 anime](./genres%20trend%20recent%20\(top%205\).png)

This shows the change in distribution of genres of top **10** anime:

![popular genres for top 10 anime](./genres%20trend%20recent%20\(top%2010\).png)

As shown by both graphs, genre Comedy, Action, Shounen (youngster), Drama, and School are the most popular in the last 5 years, and those of genre Supernatural has decreasing popularity. Other genres are not as consistently popular as the top 5 genres, nor is there a band that is continously increasing in width, thus we conclude there isn’t a specific genre that has a significant increase in popularity in the past 5 years that’s consistent enough in which anime production companies should focus on more instead immediately.

While the two stacked area graphs above help us understand recent trends, it fails to convey meaningful information when used to illustrate change in popular genres over the entire anime history, even with the consistency requirement. Therefore, we **drop the consistency requirement** and instead use the following heatmap to more intuitively and precisely demonstrate the distribution of popular genres of top 10 animes in each season for all seasons in the full dataset:

![genres for top 10 anime in anime history](./genres%20heatmap.png)

We can observe that our top 5 genres are indeed popular in most times, especially Comedy has the brightest strip over the entire history. Supernatural become popular recently but audiences are starting to lose interest in it. Space and Mecha (giant robots) seem to be genres of the past and is no longer popular anymore. We can see sparkles of Game and Harem (polygynous/polyandrous relationships). Thriller, Vampire, and Yuri (girls love) remains niche culture.

### Of Research Question 2

The mean squared error (MSE) between the predicted value and the actual score in the dataset is consistently about ***0.6*** (as shown in the output below), approximately meaning that our prediction will differ from the actual score by about 0.8 on a 10 point scale. This result is definitely not idea, but we argue it works okay when all features it requests for are present.

```diff
~ python3 ml_model.py
Model, All Features
+    MSE for train: 0.0024407141187470774
-    MSE for test : 0.6139560924369748
Model, No Duration/Episodes
+    MSE for train: 0.02175004207573632
-    MSE for test : 0.8209756239106754
~ python3 ml_model.py
Model, All Features
+    MSE for train: 0.0025445009350163615
-    MSE for test : 0.6304989379084966
Model, No Duration/Episodes
+    MSE for train: 0.027270679306084285
-    MSE for test : 0.6662676034469343
~ python3 ml_model.py
Model, All Features
+    MSE for train: 0.002390217391304347
-    MSE for test : 0.6289949852163087
Model, No Duration/Episodes
+    MSE for train: 0.026618861868029118
-    MSE for test : 0.6763534954585009
```

Looking at the trained decision tree (illustrated in [model.pdf](./model.pdf)), the order of factors it considers is `Duration`, `Source`, and (number of) `Episodes` in most of the early decisions, then later branches are based off each `genre` (e.g. Action)/`Rating` (e.g. PG-13)/`Season` (e.g. winter). Specifically, `Duration` and `Episodes` usually appear several times in the decision process. This make sense because those factors usually relate to funding available and efforts dedicated for animes’ productions. `Source`, especially animes whether if source is *Manga* is a major determiner. One possible explanation is because a manage will only be animated if its already popular. And for it has a lot of visual references, it’s easier to animate comparing to other sources like visual novels (which only have a few illustrations).

This dependency on `Duration` per episode and number of `Episodes`, rather than MSE, however, presents a severe issue when such model is used to predict score for future anime. MyAnimeList doesn’t have information about `Duration` per episode or number of `Episodes` for many of the upcoming animes, causing the above model to perform worse than measured. Therefore, another model is trained without considering for either `Duration` or `Episodes`. This model has a slightly higher MSE (as shown in the output above, under “Model, No Duration/Episodes”) as expected, but it is still acceptable. Therefore we proceed to predict the score for future anime and include the results in [predictions.csv](./predictions.csv) as `Score (adjusted)`. In a real-life scenario, anime production company have information about the anime’s episodes count and per episode length, therefore score predicted with the all features model is still included as `Score` in [predictions.csv](./predictions.csv). To illustrate the difference between the two, we included a `Score (difference)` column.

A portion of [predictions.csv](./predictions.csv) is included here for quick preview. The first entry, the final season of [Oregairu](https://www.tbs.co.jp/anime/oregairu/) (*My Youth Romantic Comedy Is Wrong, As I Expected*) has a predicted score of ***8.05*** with the adjusted model. This is similar to scores it had for the previous two season ([8.09](https://myanimelist.net/anime/14813) and [8.28](https://myanimelist.net/anime/23847) respectively).

<details>
<summary>Predictions - Spring 2020</summary>

| Name                                                         | Japanese                                                     | Score | Score (adjusted) | Score (difference) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ----- | ---------------- | ------------------ |
| Yahari Ore no Seishun Love Comedy wa Machigatteiru Kan       | やはり俺の青春ラブコメはまちがっている。完                   | 5.68  | 8.05             | 2.37               |
| Kaguya-sama wa Kokurasetai Tensai-tachi no Renai  Zunousen   | かぐや様は告らせたい？～天才たちの恋愛頭脳戦～               | 5.38  | 7.08             | 1.70               |
| Sword Art Online Alicization - War of Underworld 2nd  Season | ソードアート・オンライン アリシゼーション War of Underworld  | 5.62  | 7.27             | 1.65               |
| Shokugeki no Souma Gou no Sara                               | 食戟のソーマ 豪ノ皿                                          | 6.08  | 6.61             | 0.53               |
| Fruits Basket 2nd Season                                     | フルーツバスケット 2nd season                                | 6.66  | 8.98             | 2.32               |
| Honzuki no Gekokujou Shisho ni Naru Tame ni wa Shudan  wo Erandeiraremasen 2nd Season | 本好きの下剋上 ～司書になるためには手段を選んでいられません～ 第2期 | 6.72  | 5.66             | -1.06              |
| Kami no Tou                                                  | 神之塔  -Tower of God-                                       | 5.65  | 5.75             | 0.10               |
| Otome Game no Hametsu Flag shika Nai Akuyaku Reijou ni  Tensei shiteshimatta | 乙女ゲームの破滅フラグしかない悪役令嬢に転生してしまった…    | 6.17  | 6.55             | 0.38               |
| No Guns Life 2nd Season                                      | ノー・ガンズ・ライフ                                         | 3.97  | 6.03             | 2.06               |
| Gleipnir                                                     | グレイプニル                                                 | 5.85  | 7.28             | 1.43               |
| BNA                                                          | BNA ビー・エヌ・エー                                         | 5.65  | 6.07             | 0.42               |
| Yesterday wo Utatte                                          | イエスタデイをうたって                                       | 6.06  | 5.75             | -0.31              |
| Tsugu Tsugumomo                                              | 続・つぐもも                                                 | 6.34  | 5.96             | -0.38              |
| Kakushigoto TV                                               | かくしごと                                                   | 5.91  | 7.68             | 1.77               |
| Appare-Ranman                                                | 天晴爛漫！                                                   | 5.65  | 7.35             | 1.70               |
| Hachi-nan tte Sore wa Nai deshou                             | 八男って、それはないでしょう！                               | 5.65  | 6.05             | 0.40               |
| Digimon Adventure                                            | デジモンアドベンチャー:                                      | 6.17  | 6.82             | 0.65               |
| Jashin-chan Dropkick                                         | 邪神ちゃんドロップキック'（ダッシュ）                        | 5.38  | 7.55             | 2.17               |
| Arte                                                         | アルテ                                                       | 6.47  | 5.75             | -0.72              |
| Yu☆Gi☆Oh Sevens                                              | 遊☆戯☆王SEVENS                                               | 5.31  | 6.89             | 1.58               |
| Kingdom 3rd Season                                           | キングダム 第3シリーズ                                       | 5.65  | 6.80             | 1.15               |
| Fugou Keiji Balance Unlimited                                | 富豪刑事  Balance:UNLIMITED                                  | 5.65  | 6.24             | 0.59               |
| Shironeko Project Zero Chronicle                             | 白猫プロジェクトZERO  CHRONICLE                              | 5.65  | 5.91             | 0.26               |
| Tamayomi                                                     | 球詠                                                         | 5.65  | 7.29             | 1.64               |
| Nami yo Kiitekure                                            | 波よ聞いてくれ                                               | 5.38  | 6.55             | 1.17               |
| Kitsutsuki Tanteidokoro                                      | 啄木鳥探偵處                                                 | 5.65  | 6.24             | 0.59               |
| Listeners                                                    | LISTENERS                                                    | 5.65  | 7.33             | 1.68               |
| Princess Connect Re Dive                                     | プリンセスコネクト！Re:Dive                                  | 5.65  | 6.05             | 0.40               |
| Houkago Teibou Nisshi                                        | 放課後ていぼう日誌                                           | 5.68  | 7.29             | 1.61               |
| Gal to Kyouryuu                                              | ギャルと恐竜                                                 | 5.91  | 6.19             | 0.28               |
| Major 2nd TV 2nd Season                                      | メジャーセカンド                                             | 5.38  | 7.98             | 2.60               |
| Shin Sakura Taisen the Animation                             | 新サクラ大戦  the Animation                                  | 6.08  | 6.92             | 0.84               |
| Bungou to Alchemist Shinpan no Haguruma                      | 文豪とアルケミスト 〜審判ノ歯車〜                            | 5.65  | 6.05             | 0.40               |
| Shachou Battle no Jikan Desu                                 | 社長, バトルの時間です!                                      | 5.65  | 6.05             | 0.40               |
| Argonavis from BanG Dream                                    | アルゴナビス  from BanG Dream!                               | 6.34  | 5.98             | -0.36              |
| Ore no Yubi de Midarero Heitengo Futarikiri no Salon de      | 俺の指で乱れろ。～閉店後二人きりのサロンで…～                | 5.85  | 6.53             | 0.68               |
| Shadowverse TV                                               | シャドウバース                                               | 5.31  | 6.17             | 0.86               |
| Olympia Kyklos                                               | オリンピア・キュクロス                                       | 7.45  | 6.19             | -1.26              |
| Mewkledreamy                                                 | ミュークルドリーミー                                         | 6.34  | 5.98             | -0.36              |
| Cardfight Vanguard Gaiden If                                 | カードファイト!! ヴァンガード外伝 イフ-if-                   | 5.31  | 7.36             | 2.05               |
| Kiratto Pri☆chan  Season 3                                   | キラッとプリ☆チャン シーズン3                                | 6.66  | 8.00             | 1.34               |
| Motto Majime ni Fumajime Kaiketsu Zorori                     | もっと! まじめにふまじめ かいけつゾロリ                      | 5.38  | 6.47             | 1.09               |
| Tomica Kizuna Gattai Earth Granner                           | トミカ絆合体 アースグランナー                                | 6.34  | 7.33             | 0.99               |
| Gal-gaku Hijiri Girls Square Gakuin                          | ガル学. ~聖ガールズスクエア学院~                             | 6.08  | 7.16             | 1.08               |
| TV Yarou Nanaana Kaibutsu Kraken wo Oe                       | テレビ野郎 ナナーナ 怪物クラーケンを追え!                    | 5.38  | 7.24             | 1.86               |
| Neko Neko Nihonshi 5th Season                                | ねこねこ日本史 第5期                                         | 5.65  | 6.87             | 1.22               |
| Poccolies                                                    | ぽっこりーず                                                 | 7.74  | 6.84             | -0.90              |
| Norimono Man Mobile Land no Car-kun                          | のりものまん モービルランドのカークン                        | 7.46  | 7.22             | -0.24              |

</details>

<details>
<summary>Predictions - Summer 2020</summary>

| Name                                                         | Japanese                                                     | Score | Score (adjusted) | Score (difference) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ----- | ---------------- | ------------------ |
| Re Zero kara Hajimeru Isekai Seikatsu 2nd Season             | Re：ゼロから始める異世界生活                                 | 5.65  | 7.08             | 1.43               |
| Dungeon ni Deai wo Motomeru no wa Machigatteiru Darou  ka III | ダンジョンに出会いを求めるのは間違っているだろうか 3期       | 7.37  | 7.21             | -0.16              |
| Enen no Shouboutai Ni no Shou                                | 炎炎ノ消防隊 弐ノ章                                          | 6.08  | 6.63             | 0.55               |
| Mahouka Koukou no Rettousei Raihousha-hen                    | 魔法科高校の劣等生 来訪者編                                  | 7.00  | 7.13             | 0.13               |
| Haikyuu To the Top 2nd Season                                | ハイキュー!!  TO THE TOP 第2期                               | 5.42  | 7.98             | 2.56               |
| Kanojo Okarishimasu                                          | 彼女,  お借りします                                          | 7.11  | 7.25             | 0.14               |
| Maou Gakuin no Futekigousha Shijou Saikyou no Maou no  Shiso Tensei shite Shison-tachi no Gakkou e | 魔王学院の不適合者 ～史上最強の魔王の始祖、転生して子孫たちの学校へ通う～ | 5.65  | 5.91             | 0.26               |
| Great Pretender                                              |                                                              | 6.13  | 6.99             | 0.86               |
| Peter Grill to Kenja no Jikan                                | ピーター・グリルと賢者の時間                                 | 7.11  | 7.29             | 0.18               |
| Muhyo to Rouji no Mahouritsu Soudan Jimusho 2nd Season       | ムヒョとロージーの魔法律相談事務所 2期                       | 5.51  | 8.22             | 2.71               |
| Assault Lily Bouquet                                         | アサルトリリィ Bouquet                                       | 6.34  | 6.68             | 0.34               |
| Uzaki-chan wa Asobitai                                       | 宇崎ちゃんは遊びたい！                                       | 6.01  | 7.37             | 1.36               |
| Ex-Arm                                                       | EX-ARM                                                       | 5.85  | 6.67             | 0.82               |
| Gibiate                                                      | ジビエート                                                   | 5.65  | 7.03             | 1.38               |
| Dokyuu Hentai HxEros                                         | ド級編隊エグゼロス                                           | 7.11  | 6.63             | -0.48              |
| Tsukiuta The Animation 2                                     | ツキウタ.  THE ANIMATION 2                                   | 6.08  | 4.76             | -1.32              |
| Maesetsu                                                     | まえせつ!                                                    | 6.01  | 7.22             | 1.21               |
| Chou Futsuu Toshi Kashiwa Densetsu                           | 超普通都市カシワ伝説                                         | 5.70  | 7.39             | 1.69               |
| Obake Zukan                                                  | おばけずかん                                                 | 7.11  | 6.62             | -0.49              |
| Akudama Drive                                                | アクダマドライブ                                             | 5.65  | 6.99             | 1.34               |

</details>

#### Concerns and Future Directions

The MSE for testing dataset is much higher than the training dataset (see the output above, the first row in each cluster), indicating that our model is overfitted. To get better results than ours, one could restrict number of features, depth of the decision tree, or other hyperparameters for the `DecisionTreeRegressor`. We decide not to for the interest of time and that we didn’t learn the techniques for hyper-parameter optimization through CSE 163 with the permission of assigned mentor.

We intentionally left out information such as staffs, licensors, studios, and more. Indeed, these are important factors that audiences consider when it comes to which anime to watch in real life scenarios. Considering those factors will likely make our model more accurate as a famous voice actor is likely related to a higher score (just like movie stars). However, this can lead to further overfitting and, more importantly, is unfair for those individuals and corporations who participates in anime production for the first time. 

## Reproducing Results

> **Note**: your machine learning model might be slightly different than ours because training and testing dataset are split randomly each time the program is executed. However, they should be similar.

First, install the needed dependencies by running:

```sh
pip install -r requirements.txt
```

To derive the two research questions’ results, run:

```sh
python main.py
```

To derive research question 1’s results separately, run:

```sh
python trend_analysis.py
```

To derive research question 2’s results separately, run:

```sh
python ml_model.py
```

### Testing

To test all our programs, run:

```sh
python test.py
```

We use our sample dataset (a small dataset of anime information) to run and bebug the programs first, before it is performed on our full dataset.

For [build_dataset.py](./build_dataset.py), each individual parsing method was developed and tested in [a Colab notebook](https://colab.research.google.com/drive/1aKcL9trOFRcuVnPGRYPMb93z8khnuFjr) with cached webpages (fetched using requests). Only after the methods produce desired outputs are they then integrated into the actual file.

## Behind the Scene

### Collaboration

While we are using GitHub/git version control system to manage source code, we sat together do pair programming. Later, we switched to WeChat voice call instead to comply with the policies of social distancing made to avoid the prevailing corona virus. In either case, both of us work on the source code at the same time using Visual Studio Live Share. This process is efficient and successful, allowing both us can switch between “driver” and “navigator” easily.

For documentation/reports, we are using SharePoint (Office 365) to edit the documents at the same time in similar settings.

### Work Plan

Not as accurate as the work plan detailed below. We only used one night to fetch all the data for all animes. We started making the visualization and training the machine learning model in the last few days to finish the work. We use another extra day to modify and finalize the final report and slides. Our work plan is quite good for we left enough time to debug our programs and check and fix the errors. However, the time left for finishing the report is quite tight and forced us to focus on rushing the writing of the results parts as well as revising the whole report. 

> **Fun Fact**: the total time (as recorded by WakaTime) spent on writing code (not on writing report) is 12 hours total (if added up together).

<details>
<summary>The “Work Plan”</summary>

1. Run the dataset creation script to fetch data for all animes (**expected few days, actual 1 night**)
   1. This process needs few supervisions. We have completed the script and should not need any major modifications. **We did end up fixing a minor parsing issue for future anime.**
   2. We have full control over the dataset creation, hence there’s minimum need to perform clean up.
2. Make visualization for popular anime genre trend (**expected & actual 3 days**)
   1. Use Pandas to filter the data we need for data visualization.
   2. Use seaborn and/or Matplotlib to plot the data.
   3. Save the plot to a file for future analysis.
3. Make machine learning model to predict future anime performance (**expected & actual 3 days**)
   1. Use Pandas to filter the data we need for our ML model.
   2. Split the data into train and test set.
   3. Use DecisionTreeRegressor to train the model.
   4. Test the model.
4. Write final report (**expected 1 day, actual 2 days**)
</details>
