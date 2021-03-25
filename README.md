# Kingdom Royale Bot

## A discord bot to play Hakomari's Kingdom Royale Game.

We created this discord bot to help organizing the room's, classes, "Players", selecting targets and more.

List of commands:

* /helpMe Shows a short list of commands.

* /reg Register yourself to play the game.

* /mode [mode] Modes Available: Solo, Pairs.

* /start Start the game with current registered players.

* /choose [member_name] Choose a player of the game as partner for secreet meeting (if name has spaces, quote it with "\").

* /classC [class_name one of King, Sorcerer, Knight, Prince, Double, Revolutionary] If you are the [Player] you can choose your class.

* /Murder [member_name] If you are able to select, you can choose someone to be marked to die.\n /Assassination [member_name] If you are the revolutionary, you can select someone to die.

* /Sorcery If you are the sorcerer, you burn the one marked to death.

* /Deathblow If you are the knight you can kill the one marked if the sorcerer is dead.

* /Substitution If you are the King you can prevent being killed by assassination changing roles with the Double.

* /Strike [member_name] You can strike someone with your knife.

* /cleanMess to clean the server.

  

#### 1. Introduction

Kingdom Royale is a game adapted from a light novel called Utsuro no Hako to Zero no Maria (HakoMari). Kingdom Royale was adapted from a game with the same name that took place throughout volumes 3 and 4. Kingdom Royale requires concentration and attention to detail. The rules were made with the aim of maximizing the likelihood with the original game.

#### 2 Necessary conditions

Number of players: Currently exactly 6 people are required to play Kingdom Royale.

#### 3 The game

##### Classes

Each of the 6 players has its own class, each with different victory conditions and skills.

- He is the king who has ascended to the throne by assassinating the previous ruler and has carried out many invasions. Having a distrustful personality, he's scheming murder of the ones that threaten his throne. He does not notice that his distrust makes others lose their loyalty for him. He can request his subordinates to commit [murder], but he cannot force them because he fears their animosity could become directed at him. A land ruled by a man that cannot trust others is unlikely to have a bright future.
- Prince An ambitious person. He was originally only at the third place in the inheritance order of the king's rank. But taking advantage of the king's mistrust, he made him murder the other princes and moved up to the first place. He acquired anti-magic to guard himself against this mistrust. If he comes to the throne, this land is likely to turn into a worse dictatorship than it was before.
- The Double An ex-farmer who is loyal to the [King] and looks exactly the same as him. He is not really ambitious, but he can absolutely not allow the [Prince] to become the king since he was always made a fool by him. If he, with no ideals, becomes the king, this land is likely to fall into ruin in no time.

- Sorcerer A subordinate of the [King]. He is the teacher of the [Prince] in magic and also gets on well with the [Prince]. He is satisfied as long he can pursue his studies in magic and has no interest in the king's throne whatsoever. No matter how much he can raise his magic skills, nobody will value a person that secludes himself in his shell.
- Knight A subordinate of the [King]. While being a subordinate, he is plotting revenge on the royal family for they have ruined his homeland. He believes firmly that he can only attain happiness by exterminating the royal family. As a matter of course, a man that has drowned in his own feelings of loss will only fall into the darkness of misfortune.
- Revolutionary He is the right arm of the [King]. Because of his competence, he realized that this land is going to fall into ruin if it goes on like this. Hence, he prepared himself to take over the land. A ruler that has accumulated feelings of bitterness due to assassinations is incapable of leading a kingdom. At most he will be assassinated himself.

##### Winning conditions

As mentioned earlier, each class has its specific victory condition.

- King To protect his throne. (Elimination of the ones that threaten the king's throne - [Prince] [Revolutionary])
- Prince To become the king. (Elimination of [King] [The Double] [Revolutionary]).
- The Double Death of the ones that try to kill him. (Death of [Prince] [Revolutionary]).
- Sorcerer To survive.
- Knight To take revenge. (Death of [King] [Prince]).
- Revolutionary To become the king. (Murder of [King] [Prince] [The Double])

\* The game ends when all victory conditions for the remaining players have been met.

#### Skills

Each class has its own specific skill. 

* King
* * [Murder] He can select a player he wants to kill and request the [Sorcerer] or the [Knight] to execute this action. He does not need to select.
* * [Substituition] He can once avoid being the target of [Assassination] by changing roles with [The Double] for a single day. If he was selected as the target on this day, [The Double] will die instead of the [King].
* Prince 
* * [Throne succession] He becomes able to use [Murder] once the [King] and [The Double] die.

- * [Anti-magic] He cannot be killed by [Sorcery].

* The Double

- * [Inheritance] If the [King] dies or [Substitution] was executed, he becomes able to use [Murder].

* Sorcerer

- * [Sorcery] He can choose whether to effectively kill the character that was selected by [Murder]. The targeted character will become a burnt corpse.

* Knight

- * [Deathblow] He can choose whether to effectively kill the character that was selected by [Murder]. Only executable when the [Sorcerer] is dead. The targeted character will die due to beheading.

* Revolutionary

- * [Assassination] He can assassinate the selected character. He does not need to select one. The targeted character will become a strangulated corpse.

#### Timetable

~12 <A>

- Break, standby in own room.

12 ~ 14 <B>

- Gathering in the big room.

14 ~ 18 <C>

- Selection of [Secret Meeting] partner until 14:40. Spend 30 minutes in the room of the selected character.
- The [King] is able to select a target for [Murder].
- The [Sorcerer] can use [Sorcery] (the [Knight] can use [Deathblow]).
- (The character that was targeted by [Sorcery] or [Deathblow] will die at 17:55)

18 ~ 20 <D>

- Gathering in the big room.

20 ~ 22 <E>

- Dinner in own room.
-  The [Revolutionary] can use [Assassination].
- (The character that was targeted by [Assassination] will immediately die).

22 <F>

- Break, sleep.



#### [Player]

The [Player] works as follows: he can choose his own class with a restriction that will increase according to the number of the round. In the first round, whether N is initially the number of rounds de nido, the [Player] may choose between 6 - N classes, the others will be blocked from the choice by voting by the players. In addition, the [Player] will have an increased score according to the implementation of points. For now, it will be raffled and cannot be twice in a row.

##### Stab system

To increase the likelihood, a stabbing system was added. Each person can stab a day. The person has at most the number of players alive - 1 lives. Each day the person regains 1 life.

##### Rounds

The number of rounds must be agreed in advance. During the rounds players will be able to accumulate points, the ranking will be made from those accumulated points. The maximum number of rounds should be 6 and preferably greater than or equal to 3.

##### Score

The score system is simple, if you win, you gain one point, with you lose, nothing happens, unless you are the Player, than you lose everything.

##### Modes


Kingdom Royale can be played in two formats: two pairs and two solos or all solos. In the case of pairs, they cannot betray each other, unless one of them is [Player]. If 7 days pass, everyone wins (except for the [Player]).

