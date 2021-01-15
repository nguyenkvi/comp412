//NAME: Vi Nguyen
//NETID: vkn1
//SIM INPUT:
//OUTPUT: 1 1 2 5 15 52 203

// Computes the first 7 Bell numbers by constructing a Bell triangle
// Example usage: ./sim < vkn1.i

// Keep a 1 in a register as a hack for copying using multiplication
loadI 1 => r0

// Row 1
loadI 1 => r1

// Row 2
mult r1,r0 => r2
add r1,r2 => r3

// Row 3
mult r3,r0 => r4
add r2,r4 => r5
add r3,r5 => r6

// Row 4
mult r6,r0 => r7
add r4,r7 => r8
add r5,r8 => r9
add r6,r9 => r10

// Row 5
mult r10,r0 => r11
add r7,r11 => r12
add r8,r12 => r13
add r9,r13 => r14
add r10,r14 => r15

// Row 6
mult r15,r0 => r16
add r11,r16 => r17
add r12,r17 => r18
add r13,r18 => r19
add r14,r19 => r20
add r15,r20 => r21

// Output left side of triangle and lower right corner
loadI 1024 => r51
loadI 1028 => r52
loadI 1032 => r53
loadI 1036 => r54
loadI 1040 => r55
loadI 1044 => r56
loadI 1048 => r57

store r1 => r51
store r2 => r52
store r4 => r53
store r7 => r54
store r11 => r55
store r16 => r56
store r21 => r57

output 1024
output 1028
output 1032
output 1036
output 1040
output 1044
output 1048

