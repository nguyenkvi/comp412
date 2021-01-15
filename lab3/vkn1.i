//NAME: Vi Nguyen
//NETID: vkn1
//SIM INPUT: -i 1024 17 38
//OUTPUT: 17 38

//This test lock assumes that addresses start at 1024, as provided by -i
//The expected output of this block is 17 38, the two initial values.
//They will be manipulated by this test block but should not swap
//positions at any point, if the dependency graph produced after
//simplification is correct.

//This test block tests that the scheduler properly checks the
//independence of memops. It should not remove edges between memops
//whose virtual registers contain the same value.

//Initialize several registers to the same values.
loadI 1024 => r1
loadI 1024 => r2
loadI 1024 => r3
loadI 1028 => r4
loadI 1028 => r5
loadI 1028 => r6

load r1 => r10
load r4 => r11
store r10 => r2
store r11 => r5
load r3 => r23
load r6 => r99
store r23 => r1
store r99 => r4

store r10 => r1
store r11 => r4

output 1024
output 1028
