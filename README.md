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

- King He is the king who ascended the throne, after murdering the former ruler and who led several invasions. He is disinherited, and plans to assassinate all those who threaten his throne. He doesn't realize that his distrust causes others to lose their loyalty to him. He can ask his subordinates to commit murders, but he cannot force them, for fear that they might turn against him. A land led by a man unable to trust others will hardly have a bright future ahead of him.
- Prince An ambitious person. Originally the third in the line to receive the throne. But taking advantage of the king's distrust, he made him murder the other princes and was moved to the first in the la. To protect himself from the king's distrust he obtained anti-magic. If he comes to the throne, that country is likely to become a worse dictatorship than it was before.
- The Double A former farmer who is loyal to [King] and looks exactly like him. He is not really ambitious, but he cannot allow [Prince] to become king, since he has always been made a fool of by him. If he, who has no ideals, becomes king, that country will likely fall to ruins in no time.

- [King]'s Subordinate Sorcerer. He's [Prince's] magic teacher and gets along with him. You will be satisfied as long as you can study magic and have no interest in the royal throne. No matter how much he increases his magical abilities, no one will value someone who isolates himself in his own shell.
- [King] 's Subordinate Knight. Despite being his subordinate, the knight is planning to take revenge on the royal family that ruined his country. He strongly believes that he can only achieve happiness by exterminating the royal family. Obviously, a man drowning in his own feelings of loss will only fall into misery and darkness.
- Revolutionary He's [King's] right hand man. By his competence, he realized that the nation will fall into ruins if it continues as it is. Therefore, it is preparing to take the throne. A ruler who has accumulated bitter feelings after committing so many murders is unable to lead a nation. At most, he himself will end up murdered.

##### Winning conditions

As mentioned earlier, each class has its specific victory condition.

- King Protect your throne. (Elimination of those who threaten the king's throne - [Prince] [Revolutionary]).
- Prince Become the king. (Elimination of [King] [The Double] [Revolutionary]).
- The Double Death of those who try to kill you. (Death of [Prince] [Revolutionary]).
- Sorcerer Survive.
- Knight To take revenge. (Death of [King] [Prince]).
- Revolutionary

Become the king. (Death of [King] [Prince] [The Double]).

3. Skills

Each class has its own specific skill. 

* King
* * [Murder] He can select a player he wants to kill and request [Sorcerer] or [Knight] to perform the action. He does not need to select.
* * [Substituition] He can avoid being the target of [Assassination] once, switching places with [The Double] for a single day. If he is targeted for [Assassination] that day, [The Double] will die in place of [King].
* Prince 
* * [Throne succession] He becomes able to use [Murder] as soon as [King] and [The Double] die.

- * [Anti-magic] He cannot be killed by [Sorcery].

* The Double

- * [Inheritance] If [King] dies or [Substitution] is used, he is able to use [Murder].

* Sorcerer

- * [Sorcery] He can choose whether to effectively kill the target selected by [Murder]. The marked person will become a burnt corpse.

* Knight

- * [Deathblow] He can choose whether to effectively kill the target selected by [Murder]. Available only when [Sorcerer] is dead. The person will die by beheading.

* Revolutionary

- * [Assassination] He can select a target to be killed. He does not need to select. The person will become a strangled corpse.

#### Timetable

12 <A>

- Pause, stay in your own room.

12 ~ 14 <B>

- Meeting in the big room.

14 ~ 18 <C>

- Selection of the partner for the [Secret Meeting] until 14:40. Stay 30 minutes in the selected person's room.
- [King] is able to select a target for [Murder].
- [Sorcerer] can use [Sorcery] ([Knight] can use [Deathblow]). (The person marked by [Sorcery] or [Deathblow] will die at 17:55)

18 ~ 20 <D>

- Meeting in the big room.

20 ~ 22 <E>

- Dinner in the room.
- [Revolutionary] can use [Assassination].

(The person who is marked by [Assassination] will die immediately)

22 <F>

- Pause, sleep.



#### [Player]



The [Player] works as follows: he can choose his own class with a restriction that will increase according to the number of the round. In the first round, whether N is initially the number of rounds de nido, the [Player] may choose between 6 - N classes, the others will be blocked from the choice by voting by the players. In addition, the [Player] will have an increased score according to the implementation of points. For now, it will be raffled and cannot be twice in a row.

##### Stab system



To increase the likelihood, a stabbing system was added. Each person can stab a day. The person has at most the number of players alive - 1 lives. Each day the person regains 1 life.

##### Rounds



The number of rounds must be agreed in advance. During the rounds players will be able to accumulate points, the ranking will be made from those accumulated points. The maximum number of rounds should be 6 and preferably greater than or equal to 3.

##### Score



The score system is simple, if you win, you gain one point, with you lose, nothing happens, unless you are the Player, than you lose everything.

##### Modes



Kingdom Royale can be played in two formats: two doubles and two solos or all solos. In the case of pairs, they cannot betray each other, unless one of them is [Player]. If 7 days pass, everyone wins (except for the [Player]).

