# Callers of Multigrain target functions (for argument recovery)

---
## callers of `0x08026754` (FUN_08026754)

### `FUN_08012b24` @ `08012b24`
```c

void FUN_08012b24(undefined4 param_1)

{
  code *pcVar1;
  code *pcVar2;
  int iVar3;
  int iVar4;
  char cVar5;
  undefined *puVar6;
  int iVar7;
  int iVar8;
  char local_29 [5];
  
  pcVar1 = DAT_08012c50;
  iVar7 = DAT_08012c4c;
  iVar3 = DAT_08012c3c;
  puVar6 = (undefined *)0x0;
  iVar8 = 0;
  FUN_08026754(param_1,DAT_08012c3c + -0x4e4);
  do {
    cVar5 = *(char *)(iVar3 + 0xb8);
    if (cVar5 == '\x01') {
      iVar4 = FUN_080129b0(1,iVar3 + 0x1e4,iVar8);
      if (iVar4 == 0) {
        cVar5 = *(char *)(iVar3 + 0x1e4);
        if (cVar5 != '\0') {
          cVar5 = '\x01';
        }
      }
      else {
LAB_08012bf6:
        cVar5 = '\0';
      }
LAB_08012b58:
      pcVar2 = **(code ***)(iVar3 + -4);
      if (pcVar2 == pcVar1) goto LAB_08012b64;
LAB_08012bea:
      (*pcVar2)(iVar3 + -4,cVar5);
    }
    else {
      if (cVar5 == '\x02') {
        iVar4 = FUN_080129b0(2,iVar3 + 0xd0,iVar8);
        if (iVar4 != 0) goto LAB_08012bf6;
        cVar5 = *(char *)(iVar3 + 0xd0);
        if (cVar5 != '\0') {
          cVar5 = '\x01';
        }
        goto LAB_08012b58;
      }
      if (cVar5 != '\0') {
        cVar5 = '\0';
        iVar4 = 0;
        goto LAB_08012b58;
      }
      iVar4 = FUN_080129b0(0,iVar3 + 0x2f8,iVar8);
      if (iVar4 != 0) goto LAB_08012bf6;
      cVar5 = *(char *)(iVar3 + 0x2f8);
      pcVar2 = **(code ***)(iVar3 + -4);
      if (cVar5 != '\0') {
        cVar5 = '\x01';
      }
      if (pcVar2 != pcVar1) goto LAB_08012bea;
LAB_08012b64:
      if ((*(char *)(iVar3 + 0x10) != cVar5) &&
         (*(char *)(iVar3 + 0x10) = cVar5, *(int *)(iVar3 + 8) != 0)) {
        local_29[0] = cVar5;
        (**(code **)(iVar3 + 0xc))(iVar3,local_29);
      }
    }
    if (cVar5 != '\0') {
      FUN_0801eb10(iVar8);
    }
    if (iVar4 == 0) {
      *(undefined4 *)(iVar7 + 0x1e0) = 0;
      *(undefined4 *)(iVar7 + 0x1e4) = 0;
    }
    iVar4 = DAT_08012c44;
    puVar6 = puVar6 + 0x9f0;
    iVar8 = iVar8 + 1;
    iVar7 = iVar7 + 0x10;
    iVar3 = iVar3 + 0x9f0;
    if (puVar6 == &DAT_00004f80) {
      (**(code **)(**DAT_08012c40 + 0x40))(*DAT_08012c40,*(undefined *)(DAT_08012c44 + 0xfc4));
      *(uint *)(DAT_08012c48 + 0x1c) = (uint)*(byte *)(iVar4 + 0xfac);
      return;
    }
  } while( true );
}


```

---
## callers of `0x0801f0d4` (FUN_0801f0d4)

### `FUN_0801facc` @ `0801facc`
```c

void FUN_0801facc(void)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  
  puVar1 = (undefined4 *)(DAT_0801fb60 + 4);
  *puVar1 = DAT_0801fb64;
  FUN_0803fb34(puVar1);
  FUN_08056428(DAT_0801fb68,0,0x60);
  iVar3 = FUN_08052a94(DAT_0801fb70,DAT_0801fb6c);
  if ((iVar3 == 0) &&
     (iVar3 = FUN_0802fbf0(), uVar2 = DAT_0801fb78, puVar1 = DAT_0801fb74, iVar3 == 0)) {
    *DAT_0801fb74 = 1;
    FUN_0804cb58(uVar2);
    FUN_08051058(DAT_0801fb80,DAT_0801fb7c,1);
    uVar4 = FUN_0805253c(DAT_0801fb84);
    if (((uVar4 & 0xf7) != 0) || (uVar4 = FUN_0805253c(DAT_0801fb8c), (uVar4 & 0xf7) != 0)) {
      FUN_0804cb58(DAT_0801fb88);
      return;
    }
    uVar4 = FUN_0805253c(DAT_0801fb90);
    FUN_0804cb58(DAT_0801fb88);
    if (((((uVar4 & 0xf7) == 0) && (iVar3 = FUN_0801ebf4(), iVar3 == 0)) &&
        (iVar3 = FUN_0801f848(), iVar3 == 0)) && (iVar3 = FUN_0801f0d4(), iVar3 == 0)) {
      *puVar1 = 0;
      return;
    }
  }
  return;
}


```

---
## callers of `0x08024414` (FUN_08024414)

### `FUN_08024598` @ `08024598`
```c

uint FUN_08024598(uint param_1,int param_2)

{
  uint *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  uint *puVar4;
  uint uVar5;
  int iVar6;
  int iVar7;
  uint uVar8;
  uint uVar9;
  int iVar10;
  uint *puVar11;
  uint uVar12;
  int iVar13;
  uint uVar14;
  int *piVar15;
  undefined local_29 [5];
  
  uVar3 = DAT_08024724;
  uVar2 = DAT_08024720;
  if (*DAT_0802471c == 3) {
    return 1;
  }
  if (0x2f < param_1) {
    return 9;
  }
  *DAT_0802471c = 1;
  FUN_080569f8(uVar3,uVar2,param_1 + 1);
  uVar2 = DAT_08024724;
  *DAT_08024728 = param_1;
  FUN_0804cb68(DAT_0802472c,uVar2);
  FUN_08051058(DAT_08024734,DAT_08024730,1);
  uVar5 = FUN_0805253c(DAT_08024724);
  if (((uVar5 & 0xf7) == 0) && (uVar5 = FUN_0801f448(), uVar5 == 0)) {
    iVar6 = FUN_08024414(DAT_08024738,param_2);
    puVar4 = DAT_0802474c;
    param_2 = param_2 + 0x5b7;
    uVar12 = 0;
    puVar11 = DAT_0802473c;
    do {
      while( true ) {
        uVar9 = puVar4[2];
        iVar13 = param_2 + 0x225;
        puVar1 = puVar11 + 1;
        *puVar1 = 0;
        puVar11[9] = 0;
        puVar11[0x11] = uVar9 - 1;
        iVar10 = DAT_08024af8;
        iVar7 = DAT_08024af4;
        if ((*(char *)(param_2 + 0x225) == '\0') || (*(char *)(param_2 + -0x1b) != '\0')) break;
        uVar9 = *puVar4;
        if ((int)uVar9 < 1) goto LAB_0802464e;
        uVar14 = uVar9 & 7;
        uVar8 = 0;
        if (uVar14 == 0) {
LAB_0802482e:
          do {
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x100,iVar13,0x100);
            uVar14 = uVar8 + 1;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x200,iVar13);
            uVar14 = uVar8 + 2;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x300,iVar13,0x100);
            uVar14 = uVar8 + 3;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x400,iVar13,0x100);
            uVar14 = uVar8 + 4;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x500,iVar13,0x100);
            uVar14 = uVar8 + 5;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = FUN_08056a38(iVar7 + 0x600,iVar13,0x100);
            uVar14 = uVar8 + 6;
            if (iVar10 == 0) goto LAB_08024adc;
            iVar10 = iVar7 + 0x700;
            uVar14 = uVar8 + 7;
            iVar7 = iVar7 + 0x800;
            iVar10 = FUN_08056a38(iVar10,iVar13,0x100);
            if (iVar10 == 0) goto LAB_08024adc;
            uVar8 = uVar8 + 8;
          } while (uVar8 != uVar9);
        }
        else {
          if (uVar14 == 1) {
LAB_0802480e:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              if (uVar8 == uVar9) goto LAB_0802464e;
              goto LAB_0802482e;
            }
          }
          else if (uVar14 == 2) {
LAB_080247f6:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              goto LAB_0802480e;
            }
          }
          else if (uVar14 == 3) {
LAB_080247de:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              goto LAB_080247f6;
            }
          }
          else if (uVar14 == 4) {
LAB_080247c6:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              goto LAB_080247de;
            }
          }
          else if (uVar14 == 5) {
LAB_080247ae:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              goto LAB_080247c6;
            }
          }
          else if (uVar14 == 6) {
LAB_08024796:
            iVar10 = FUN_08056a38(iVar7,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              uVar8 = uVar8 + 1;
              iVar7 = iVar7 + 0x100;
              goto LAB_080247ae;
            }
          }
          else {
            iVar10 = FUN_08056a38(DAT_08024af4,iVar13,0x100);
            uVar14 = uVar8;
            if (iVar10 != 0) {
              iVar7 = iVar7 + 0x100;
              uVar8 = 1;
              goto LAB_08024796;
            }
          }
LAB_08024adc:
          *puVar1 = uVar14;
        }
LAB_0802464e:
        uVar12 = uVar12 + 1;
        param_2 = param_2 + 0x9f0;
        puVar11 = puVar1;
        if (uVar12 == 8) goto LAB_080246da;
      }
      if ((iVar6 == 0) || ((int)*puVar4 <= (int)uVar12)) {
        iVar7 = param_2 + 0x111;
        if ((*(char *)(param_2 + 0x111) == '\0') || (*(char *)(param_2 + -0x1b) != '\x01')) {
          if ((*(char *)(param_2 + -3) != '\0') &&
             ((*(char *)(param_2 + -0x1b) == '\x02' && (0 < (int)uVar9)))) {
            uVar9 = 0;
            piVar15 = DAT_08024afc;
            do {
              iVar10 = *piVar15;
              iVar7 = FUN_08055818(param_2);
              if (iVar10 == iVar7) {
                puVar11[0x11] = uVar9;
                break;
              }
              uVar9 = uVar9 + 1;
              piVar15 = piVar15 + 1;
            } while ((int)uVar9 < (int)puVar4[2]);
          }
        }
        else {
          uVar9 = puVar4[1];
          if (0 < (int)uVar9) {
            uVar8 = uVar9 & 7;
            uVar14 = 0;
            if (uVar8 == 0) {
LAB_080249f6:
              do {
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x100,iVar7,0x100);
                uVar8 = uVar14 + 1;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x200,iVar7);
                uVar8 = uVar14 + 2;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x300,iVar7,0x100);
                uVar8 = uVar14 + 3;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x400,iVar7,0x100);
                uVar8 = uVar14 + 4;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x500,iVar7,0x100);
                uVar8 = uVar14 + 5;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = FUN_08056a38(iVar10 + 0x600,iVar7,0x100);
                uVar8 = uVar14 + 6;
                if (iVar13 == 0) goto LAB_08024ae0;
                iVar13 = iVar10 + 0x700;
                uVar8 = uVar14 + 7;
                iVar10 = iVar10 + 0x800;
                iVar13 = FUN_08056a38(iVar13,iVar7,0x100);
                if (iVar13 == 0) goto LAB_08024ae0;
                uVar14 = uVar14 + 8;
              } while (uVar9 != uVar14);
            }
            else {
              if (uVar8 == 1) {
LAB_080249d6:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  if (uVar9 == uVar14) goto LAB_0802464e;
                  goto LAB_080249f6;
                }
              }
              else if (uVar8 == 2) {
LAB_080249bc:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  goto LAB_080249d6;
                }
              }
              else if (uVar8 == 3) {
LAB_080249a2:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  goto LAB_080249bc;
                }
              }
              else if (uVar8 == 4) {
LAB_08024988:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  goto LAB_080249a2;
                }
              }
              else if (uVar8 == 5) {
LAB_0802496e:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  goto LAB_08024988;
                }
              }
              else if (uVar8 == 6) {
LAB_08024954:
                iVar13 = FUN_08056a38(iVar10,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  uVar14 = uVar14 + 1;
                  iVar10 = iVar10 + 0x100;
                  goto LAB_0802496e;
                }
              }
              else {
                iVar13 = FUN_08056a38(DAT_08024af8,iVar7,0x100);
                uVar8 = uVar14;
                if (iVar13 != 0) {
                  iVar10 = iVar10 + 0x100;
                  uVar14 = 1;
                  goto LAB_08024954;
                }
              }
LAB_08024ae0:
              puVar11[9] = uVar8;
            }
          }
        }
        goto LAB_0802464e;
      }
      if (**(code ***)(param_2 + -0x2f) == DAT_08024740) {
        if ((*(char *)(param_2 + -0x1b) != '\0') &&
           (*(undefined *)(param_2 + -0x1b) = 0, *(int *)(param_2 + -0x23) != 0)) {
          local_29[0] = 0;
          (**(code **)(param_2 + -0x1f))(param_2 + -0x2b,local_29);
        }
      }
      else {
        (***(code ***)(param_2 + -0x2f))(param_2 + -0x2f,0);
      }
      iVar7 = param_2 + 0x211;
      param_2 = param_2 + 0x9f0;
      FUN_0801ff08(iVar7,DAT_08024744 + uVar12 * 0x100);
      *puVar1 = uVar12;
      uVar12 = uVar12 + 1;
      puVar11 = puVar1;
    } while (uVar12 != 8);
LAB_080246da:
    *(uint *)(DAT_08024748 + (param_1 >> 5) * 4) =
         1 << (param_1 & 0x1f) | *(uint *)(DAT_08024748 + (param_1 >> 5) * 4);
  }
  else {
    if (uVar5 == 1) {
      *DAT_08024af0 = 3;
      return 1;
    }
    if (uVar5 == 0x12) {
      *DAT_0802471c = 2;
      return 0x12;
    }
  }
  *DAT_0802471c = 0;
  return uVar5;
}


```

### `FUN_08024b00` @ `08024b00`
```c

byte FUN_08024b00(uint param_1)

{
  uint *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  byte bVar8;
  int iVar9;
  undefined4 *puVar10;
  int iVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  undefined4 *puVar15;
  int iVar16;
  byte local_5117;
  char local_5116;
  byte local_5115;
  undefined4 local_5114 [3];
  undefined4 local_5108;
  undefined local_5100;
  undefined4 local_50fc;
  undefined4 local_50f0;
  undefined local_50e8;
  undefined4 local_50e4;
  undefined4 local_50d8;
  undefined auStack_50d0 [72];
  undefined auStack_5088 [304];
  undefined4 local_4f58;
  undefined4 local_4f4c;
  undefined local_4f44;
  undefined4 local_4f40;
  undefined4 local_4f34;
  undefined local_4f2c;
  undefined4 local_4f28;
  undefined4 local_4f1c;
  undefined local_4f14;
  undefined4 local_4f10;
  undefined4 local_4f04;
  undefined local_4efc;
  undefined4 local_4ef8;
  undefined4 local_4eec;
  undefined4 local_4ee4;
  undefined4 uStack_4ee0;
  undefined4 local_4ed4;
  undefined4 local_4ecc;
  undefined4 uStack_4ec8;
  undefined4 local_4ebc;
  undefined4 local_4eb4;
  undefined4 uStack_4eb0;
  undefined4 local_4ea4;
  undefined4 local_4e9c;
  undefined4 uStack_4e98;
  undefined4 local_4e8c;
  undefined local_4e84;
  undefined4 local_4e80;
  undefined4 local_4e74;
  undefined auStack_4e6c [72];
  undefined auStack_4e24 [304];
  undefined4 local_4cf4;
  undefined4 local_4ce8;
  undefined local_4ce0;
  undefined4 local_4cdc;
  undefined4 local_4cd0;
  undefined local_4cc8;
  undefined4 local_4cc4;
  undefined4 local_4cb8;
  undefined local_4cb0;
  undefined4 local_4cac;
  undefined4 local_4ca0;
  undefined local_4c98;
  undefined4 local_4c94;
  undefined4 local_4c88;
  undefined4 local_4c80;
  undefined4 local_4c7c;
  undefined4 local_4c70;
  undefined4 local_4c68;
  undefined4 local_4c64;
  undefined4 local_4c58;
  undefined4 local_4c50;
  undefined4 local_4c4c;
  undefined4 local_4c40;
  undefined4 local_4c38;
  undefined4 local_4c34;
  undefined4 local_4c28;
  undefined local_4c20;
  undefined4 local_4c1c;
  undefined4 local_4c10;
  undefined4 local_4c08;
  undefined4 local_4c04;
  undefined4 local_4bf8;
  undefined4 local_4bf0;
  undefined4 local_4bec;
  undefined4 local_4be0;
  undefined4 local_4bd8;
  undefined4 local_4bd4;
  undefined4 local_4bc8;
  undefined2 local_4bc0;
  undefined4 local_4bbc;
  undefined4 local_4bb0;
  undefined4 local_4ba8;
  undefined4 local_4ba4;
  undefined4 local_4b98;
  undefined4 local_4b90;
  undefined4 local_4b8c;
  undefined4 local_4b80;
  undefined local_4b78;
  undefined4 local_4b74;
  undefined4 local_4b68;
  undefined auStack_4b60 [256];
  undefined4 local_4a60;
  undefined4 local_4a54;
  undefined auStack_4a4c [256];
  undefined4 local_494c;
  undefined4 local_4940;
  undefined auStack_4938 [256];
  undefined4 local_4838;
  undefined4 local_482c;
  undefined4 local_4824;
  undefined4 local_4820;
  undefined4 local_4814;
  undefined4 local_480c;
  undefined4 local_4808;
  undefined4 local_4804;
  undefined4 local_4800;
  undefined4 local_47fc;
  undefined4 local_47f0;
  undefined4 local_47e8;
  undefined4 local_47e4;
  undefined4 local_47d8;
  undefined4 local_47d0;
  undefined4 local_47cc;
  undefined4 local_47c0;
  undefined4 local_47b8;
  undefined4 local_47b4;
  undefined4 local_47a8;
  undefined4 local_47a0;
  undefined4 local_479c;
  undefined4 local_4790;
  undefined local_4788;
  undefined4 local_4784;
  undefined4 local_4778;
  undefined local_4770;
  undefined4 local_476c;
  undefined4 local_4760;
  undefined local_4758;
  undefined4 local_4754;
  undefined4 local_4748;
  undefined4 local_4740;
  undefined4 local_473c;
  undefined4 local_4730;
  undefined4 local_4728;
  undefined4 local_4724;
  undefined4 local_4718;
  undefined local_4710;
  undefined4 local_470c;
  undefined4 local_4700;
  undefined local_46f8;
  undefined4 local_46f4;
  undefined4 local_46e8;
  undefined auStack_46e0 [72];
  undefined auStack_4698 [304];
  undefined4 local_4568;
  undefined4 local_455c;
  undefined local_4554;
  undefined4 local_4550;
  undefined4 local_4544;
  undefined local_453c;
  undefined4 local_4538;
  undefined4 local_452c;
  undefined local_4524;
  undefined4 local_4520;
  undefined4 local_4514;
  undefined local_450c;
  undefined4 local_4508;
  undefined4 local_44fc;
  undefined4 local_44f4;
  undefined4 local_44f0;
  undefined4 local_44e4;
  undefined4 local_44dc;
  undefined4 local_44d8;
  undefined4 local_44cc;
  undefined4 local_44c4;
  undefined4 local_44c0;
  undefined4 local_44b4;
  undefined4 local_44ac;
  undefined4 local_44a8;
  undefined4 local_449c;
  undefined local_4494;
  undefined4 local_4490;
  undefined4 local_4484;
  undefined auStack_447c [72];
  undefined auStack_4434 [304];
  undefined4 local_4304;
  undefined4 local_42f8;
  undefined local_42f0;
  undefined4 local_42ec;
  undefined4 local_42e0;
  undefined local_42d8;
  undefined4 local_42d4;
  undefined4 local_42c8;
  undefined local_42c0;
  undefined4 local_42bc;
  undefined4 local_42b0;
  undefined local_42a8;
  undefined4 local_42a4;
  undefined4 local_4298;
  undefined4 local_4290;
  undefined4 local_428c;
  undefined4 local_4280;
  undefined4 local_4278;
  undefined4 local_4274;
  undefined4 local_4268;
  undefined4 local_4260;
  undefined4 local_425c;
  undefined4 local_4250;
  undefined4 local_4248;
  undefined4 local_4244;
  undefined4 local_4238;
  undefined local_4230;
  undefined4 local_422c;
  undefined4 local_4220;
  undefined4 local_4218;
  undefined4 local_4214;
  undefined4 local_4208;
  undefined4 local_4200;
  undefined4 local_41fc;
  undefined4 local_41f0;
  undefined4 local_41e8;
  undefined4 local_41e4;
  undefined4 local_41d8;
  undefined2 local_41d0;
  undefined4 local_41cc;
  undefined4 local_41c0;
  undefined4 local_41b8;
  undefined4 local_41b4;
  undefined4 local_41a8;
  undefined4 local_41a0;
  undefined4 local_419c;
  undefined4 local_4190;
  undefined local_4188;
  undefined4 local_4184;
  undefined4 local_4178;
  undefined auStack_4170 [256];
  undefined4 local_4070;
  undefined4 local_4064;
  undefined auStack_405c [256];
  undefined4 local_3f5c;
  undefined4 local_3f50;
  undefined auStack_3f48 [256];
  undefined4 local_3e48;
  undefined4 local_3e3c;
  undefined4 local_3e34;
  undefined4 local_3e30;
  undefined4 local_3e24;
  undefined4 local_3e1c;
  undefined4 local_3e18;
  undefined4 local_3e14;
  undefined4 local_3e10;
  undefined4 local_3e0c;
  undefined4 local_3e00;
  undefined4 local_3df8;
  undefined4 local_3df4;
  undefined4 local_3de8;
  undefined4 local_3de0;
  undefined4 local_3ddc;
  undefined4 local_3dd0;
  undefined4 local_3dc8;
  undefined4 local_3dc4;
  undefined4 local_3db8;
  undefined4 local_3db0;
  undefined4 uStack_3dac;
  undefined4 local_3da0;
  undefined local_3d98;
  undefined4 local_3d94;
  undefined4 local_3d88;
  undefined local_3d80;
  undefined4 local_3d7c;
  undefined4 local_3d70;
  undefined local_3d68;
  undefined4 local_3d64;
  undefined4 local_3d58;
  undefined4 local_3d50;
  undefined4 uStack_3d4c;
  undefined4 local_3d40;
  undefined4 local_3d38;
  undefined4 uStack_3d34;
  undefined4 local_3d28;
  undefined local_3d20;
  undefined4 local_3d1c;
  undefined4 local_3d10;
  undefined local_3d08;
  undefined4 local_3d04;
  undefined4 local_3cf8;
  undefined auStack_3cf0 [72];
  undefined auStack_3ca8 [304];
  undefined4 local_3b78;
  undefined4 local_3b6c;
  undefined local_3b64;
  undefined4 local_3b60;
  undefined4 local_3b54;
  undefined local_3b4c;
  undefined4 local_3b48;
  undefined4 local_3b3c;
  undefined local_3b34;
  undefined4 local_3b30;
  undefined4 local_3b24;
  undefined local_3b1c;
  undefined4 local_3b18;
  undefined4 local_3b0c;
  undefined4 local_3b04;
  undefined4 local_3b00;
  undefined4 local_3af4;
  undefined4 local_3aec;
  undefined4 local_3ae8;
  undefined4 local_3adc;
  undefined4 local_3ad4;
  undefined4 local_3ad0;
  undefined4 local_3ac4;
  undefined4 local_3abc;
  undefined4 local_3ab8;
  undefined4 local_3aac;
  undefined local_3aa4;
  undefined4 local_3aa0;
  undefined4 local_3a94;
  undefined auStack_3a8c [72];
  undefined auStack_3a44 [304];
  undefined4 local_3914;
  undefined4 local_3908;
  undefined local_3900;
  undefined4 local_38fc;
  undefined4 local_38f0;
  undefined local_38e8;
  undefined4 local_38e4;
  undefined4 local_38d8;
  undefined local_38d0;
  undefined4 local_38cc;
  undefined4 local_38c0;
  undefined local_38b8;
  undefined4 local_38b4;
  undefined4 local_38a8;
  undefined4 local_38a0;
  undefined4 local_389c;
  undefined4 local_3890;
  undefined4 local_3888;
  undefined4 local_3884;
  undefined4 local_3878;
  undefined4 local_3870;
  undefined4 local_386c;
  undefined4 local_3860;
  undefined4 local_3858;
  undefined4 local_3854;
  undefined4 local_3848;
  undefined local_3840;
  undefined4 local_383c;
  undefined4 local_3830;
  undefined4 local_3828;
  undefined4 local_3824;
  undefined4 local_3818;
  undefined4 local_3810;
  undefined4 local_380c;
  undefined4 local_3800;
  undefined4 local_37f8;
  undefined4 local_37f4;
  undefined4 local_37e8;
  undefined2 local_37e0;
  undefined4 local_37dc;
  undefined4 local_37d0;
  undefined4 local_37c8;
  undefined4 local_37c4;
  undefined4 local_37b8;
  undefined4 local_37b0;
  undefined4 local_37ac;
  undefined4 local_37a0;
  undefined local_3798;
  undefined4 local_3794;
  undefined4 local_3788;
  undefined auStack_3780 [256];
  undefined4 local_3680;
  undefined4 local_3674;
  undefined auStack_366c [256];
  undefined4 local_356c;
  undefined4 local_3560;
  undefined auStack_3558 [256];
  undefined4 local_3458;
  undefined4 local_344c;
  undefined4 local_3444;
  undefined4 local_3440;
  undefined4 local_3434;
  undefined4 local_342c;
  undefined4 local_3428;
  undefined4 local_3424;
  undefined4 local_3420;
  undefined4 local_341c;
  undefined4 local_3410;
  undefined4 local_3408;
  undefined4 local_3404;
  undefined4 local_33f8;
  undefined4 local_33f0;
  undefined4 local_33ec;
  undefined4 local_33e0;
  undefined4 local_33d8;
  undefined4 local_33d4;
  undefined4 local_33c8;
  undefined4 local_33c0;
  undefined4 local_33bc;
  undefined4 local_33b0;
  undefined local_33a8;
  undefined4 local_33a4;
  undefined4 local_3398;
  undefined local_3390;
  undefined4 local_338c;
  undefined4 local_3380;
  undefined local_3378;
  undefined4 local_3374;
  undefined4 local_3368;
  undefined4 local_3360;
  undefined4 local_335c;
  undefined4 local_3350;
  undefined4 local_3348;
  undefined4 local_3344;
  undefined4 local_3338;
  undefined local_3330;
  undefined4 local_332c;
  undefined4 local_3320;
  undefined local_3318;
  undefined4 local_3314;
  undefined4 local_3308;
  undefined auStack_3300 [72];
  undefined auStack_32b8 [304];
  undefined4 local_3188;
  undefined4 local_317c;
  undefined local_3174;
  undefined4 local_3170;
  undefined4 local_3164;
  undefined local_315c;
  undefined4 local_3158;
  undefined4 local_314c;
  undefined local_3144;
  undefined4 local_3140;
  undefined4 local_3134;
  undefined local_312c;
  undefined4 local_3128;
  undefined4 local_311c;
  undefined4 local_3114;
  undefined4 local_3110;
  undefined4 local_3104;
  undefined4 local_30fc;
  undefined4 local_30f8;
  undefined4 local_30ec;
  undefined4 local_30e4;
  undefined4 local_30e0;
  undefined4 local_30d4;
  undefined4 local_30cc;
  undefined4 local_30c8;
  undefined4 local_30bc;
  undefined local_30b4;
  undefined4 local_30b0;
  undefined4 local_30a4;
  undefined auStack_309c [72];
  undefined auStack_3054 [304];
  undefined4 local_2f24;
  undefined4 local_2f18;
  undefined local_2f10;
  undefined4 local_2f0c;
  undefined4 local_2f00;
  undefined local_2ef8;
  undefined4 local_2ef4;
  undefined4 local_2ee8;
  undefined local_2ee0;
  undefined4 local_2edc;
  undefined4 local_2ed0;
  undefined local_2ec8;
  undefined4 local_2ec4;
  undefined4 local_2eb8;
  undefined4 local_2eb0;
  undefined4 uStack_2eac;
  undefined4 local_2ea0;
  undefined4 local_2e98;
  undefined4 uStack_2e94;
  undefined4 local_2e88;
  undefined4 local_2e80;
  undefined4 uStack_2e7c;
  undefined4 local_2e70;
  undefined4 local_2e68;
  undefined4 uStack_2e64;
  undefined4 local_2e58;
  undefined local_2e50;
  undefined4 local_2e4c;
  undefined4 local_2e40;
  undefined4 local_2e38;
  undefined4 local_2e34;
  undefined4 local_2e28;
  undefined4 local_2e20;
  undefined4 local_2e1c;
  undefined4 local_2e10;
  undefined4 local_2e08;
  undefined4 local_2e04;
  undefined4 local_2df8;
  undefined2 local_2df0;
  undefined4 local_2dec;
  undefined4 local_2de0;
  undefined4 local_2dd8;
  undefined4 local_2dd4;
  undefined4 local_2dc8;
  undefined4 local_2dc0;
  undefined4 local_2dbc;
  undefined4 local_2db0;
  undefined local_2da8;
  undefined4 local_2da4;
  undefined4 local_2d98;
  undefined auStack_2d90 [256];
  undefined4 local_2c90;
  undefined4 local_2c84;
  undefined auStack_2c7c [256];
  undefined4 local_2b7c;
  undefined4 local_2b70;
  undefined auStack_2b68 [256];
  undefined4 local_2a68;
  undefined4 local_2a5c;
  undefined4 local_2a54;
  undefined4 local_2a50;
  undefined4 local_2a44;
  undefined4 local_2a3c;
  undefined4 local_2a38;
  undefined4 local_2a34;
  undefined4 local_2a30;
  undefined4 local_2a2c;
  undefined4 local_2a20;
  undefined4 local_2a18;
  undefined4 local_2a14;
  undefined4 local_2a08;
  undefined4 local_2a00;
  undefined4 local_29fc;
  undefined4 local_29f0;
  undefined4 local_29e8;
  undefined4 local_29e4;
  undefined4 local_29d8;
  undefined4 local_29d0;
  undefined4 local_29cc;
  undefined4 local_29c0;
  undefined local_29b8;
  undefined4 local_29b4;
  undefined4 local_29a8;
  undefined local_29a0;
  undefined4 local_299c;
  undefined4 local_2990;
  undefined local_2988;
  undefined4 local_2984;
  undefined4 local_2978;
  undefined4 local_2970;
  undefined4 local_296c;
  undefined4 local_2960;
  undefined4 local_2958;
  undefined4 local_2954;
  undefined4 local_2948;
  undefined local_2940;
  undefined4 local_293c;
  undefined4 local_2930;
  undefined local_2928;
  undefined4 local_2924;
  undefined4 local_2918;
  undefined auStack_2910 [72];
  undefined auStack_28c8 [304];
  undefined4 local_2798;
  undefined4 local_278c;
  undefined local_2784;
  undefined4 local_2780;
  undefined4 local_2774;
  undefined local_276c;
  undefined4 local_2768;
  undefined4 local_275c;
  undefined local_2754;
  undefined4 local_2750;
  undefined4 local_2744;
  undefined local_273c;
  undefined4 local_2738;
  undefined4 local_272c;
  undefined4 local_2724;
  undefined4 local_2720;
  undefined4 local_2714;
  undefined4 local_270c;
  undefined4 local_2708;
  undefined4 local_26fc;
  undefined4 local_26f4;
  undefined4 local_26f0;
  undefined4 local_26e4;
  undefined4 local_26dc;
  undefined4 local_26d8;
  undefined4 local_26cc;
  undefined local_26c4;
  undefined4 local_26c0;
  undefined4 local_26b4;
  undefined auStack_26ac [72];
  undefined auStack_2664 [304];
  undefined4 local_2534;
  undefined4 local_2528;
  undefined local_2520;
  undefined4 local_251c;
  undefined4 local_2510;
  undefined local_2508;
  undefined4 local_2504;
  undefined4 local_24f8;
  undefined local_24f0;
  undefined4 local_24ec;
  undefined4 local_24e0;
  undefined local_24d8;
  undefined4 local_24d4;
  undefined4 local_24c8;
  undefined4 local_24c0;
  undefined4 local_24bc;
  undefined4 local_24b0;
  undefined4 local_24a8;
  undefined4 local_24a4;
  undefined4 local_2498;
  undefined4 local_2490;
  undefined4 local_248c;
  undefined4 local_2480;
  undefined4 local_2478;
  undefined4 local_2474;
  undefined4 local_2468;
  undefined local_2460;
  undefined4 local_245c;
  undefined4 local_2450;
  undefined4 local_2448;
  undefined4 local_2444;
  undefined4 local_2438;
  undefined4 local_2430;
  undefined4 local_242c;
  undefined4 local_2420;
  undefined4 local_2418;
  undefined4 local_2414;
  undefined4 local_2408;
  undefined2 local_2400;
  undefined4 local_23fc;
  undefined4 local_23f0;
  undefined4 local_23e8;
  undefined4 local_23e4;
  undefined4 local_23d8;
  undefined4 local_23d0;
  undefined4 local_23cc;
  undefined4 local_23c0;
  undefined local_23b8;
  undefined4 local_23b4;
  undefined4 local_23a8;
  undefined auStack_23a0 [256];
  undefined4 local_22a0;
  undefined4 local_2294;
  undefined auStack_228c [256];
  undefined4 local_218c;
  undefined4 local_2180;
  undefined auStack_2178 [256];
  undefined4 local_2078;
  undefined4 local_206c;
  undefined4 local_2064;
  undefined4 local_2060;
  undefined4 local_2054;
  undefined4 local_204c;
  undefined4 local_2048;
  undefined4 local_2044;
  undefined4 local_2040;
  undefined4 local_203c;
  undefined4 local_2030;
  undefined4 local_2028;
  undefined4 local_2024;
  undefined4 local_2018;
  undefined4 local_2010;
  undefined4 local_200c;
  undefined4 local_2000;
  undefined4 local_1ff8;
  undefined4 local_1ff4;
  undefined4 local_1fe8;
  undefined4 local_1fe0;
  undefined4 uStack_1fdc;
  undefined4 local_1fd0;
  undefined local_1fc8;
  undefined4 local_1fc4;
  undefined4 local_1fb8;
  undefined local_1fb0;
  undefined4 local_1fac;
  undefined4 local_1fa0;
  undefined local_1f98;
  undefined4 local_1f94;
  undefined4 local_1f88;
  undefined4 local_1f80;
  undefined4 uStack_1f7c;
  undefined4 local_1f70;
  undefined4 local_1f68;
  undefined4 uStack_1f64;
  undefined4 local_1f58;
  undefined local_1f50;
  undefined4 local_1f4c;
  undefined4 local_1f40;
  undefined local_1f38;
  undefined4 local_1f34;
  undefined4 local_1f28;
  undefined auStack_1f20 [72];
  undefined auStack_1ed8 [304];
  undefined4 local_1da8;
  undefined4 local_1d9c;
  undefined local_1d94;
  undefined4 local_1d90;
  undefined4 local_1d84;
  undefined local_1d7c;
  undefined4 local_1d78;
  undefined4 local_1d6c;
  undefined local_1d64;
  undefined4 local_1d60;
  undefined4 local_1d54;
  undefined local_1d4c;
  undefined4 local_1d48;
  undefined4 local_1d3c;
  undefined4 local_1d34;
  undefined4 uStack_1d30;
  undefined4 local_1d24;
  undefined4 local_1d1c;
  undefined4 uStack_1d18;
  undefined4 local_1d0c;
  undefined4 local_1d04;
  undefined4 uStack_1d00;
  undefined4 local_1cf4;
  undefined4 local_1cec;
  undefined4 uStack_1ce8;
  undefined4 local_1cdc;
  undefined local_1cd4;
  undefined4 local_1cd0;
  undefined4 local_1cc4;
  undefined auStack_1cbc [72];
  undefined auStack_1c74 [304];
  undefined4 local_1b44;
  undefined4 local_1b38;
  undefined local_1b30;
  undefined4 local_1b2c;
  undefined4 local_1b20;
  undefined local_1b18;
  undefined4 local_1b14;
  undefined4 local_1b08;
  undefined local_1b00;
  undefined4 local_1afc;
  undefined4 local_1af0;
  undefined local_1ae8;
  undefined4 local_1ae4;
  undefined4 local_1ad8;
  undefined4 local_1ad0;
  undefined4 local_1acc;
  undefined4 local_1ac0;
  undefined4 local_1ab8;
  undefined4 local_1ab4;
  undefined4 local_1aa8;
  undefined4 local_1aa0;
  undefined4 local_1a9c;
  undefined4 local_1a90;
  undefined4 local_1a88;
  undefined4 local_1a84;
  undefined4 local_1a78;
  undefined local_1a70;
  undefined4 local_1a6c;
  undefined4 local_1a60;
  undefined4 local_1a58;
  undefined4 local_1a54;
  undefined4 local_1a48;
  undefined4 local_1a40;
  undefined4 local_1a3c;
  undefined4 local_1a30;
  undefined4 local_1a28;
  undefined4 local_1a24;
  undefined4 local_1a18;
  undefined2 local_1a10;
  undefined4 local_1a0c;
  undefined4 local_1a00;
  undefined4 local_19f8;
  undefined4 local_19f4;
  undefined4 local_19e8;
  undefined4 local_19e0;
  undefined4 local_19dc;
  undefined4 local_19d0;
  undefined local_19c8;
  undefined4 local_19c4;
  undefined4 local_19b8;
  undefined auStack_19b0 [256];
  undefined4 local_18b0;
  undefined4 local_18a4;
  undefined auStack_189c [256];
  undefined4 local_179c;
  undefined4 local_1790;
  undefined auStack_1788 [256];
  undefined4 local_1688;
  undefined4 local_167c;
  undefined4 local_1674;
  undefined4 local_1670;
  undefined4 local_1664;
  undefined4 local_165c;
  undefined4 local_1658;
  undefined4 local_1654;
  undefined4 local_1650;
  undefined4 local_164c;
  undefined4 local_1640;
  undefined4 local_1638;
  undefined4 local_1634;
  undefined4 local_1628;
  undefined4 local_1620;
  undefined4 local_161c;
  undefined4 local_1610;
  undefined4 local_1608;
  undefined4 local_1604;
  undefined4 local_15f8;
  undefined4 local_15f0;
  undefined4 local_15ec;
  undefined4 local_15e0;
  undefined local_15d8;
  undefined4 local_15d4;
  undefined4 local_15c8;
  undefined local_15c0;
  undefined4 local_15bc;
  undefined4 local_15b0;
  undefined local_15a8;
  undefined4 local_15a4;
  undefined4 local_1598;
  undefined4 local_1590;
  undefined4 local_158c;
  undefined4 local_1580;
  undefined4 local_1578;
  undefined4 local_1574;
  undefined4 local_1568;
  undefined local_1560;
  undefined4 local_155c;
  undefined4 local_1550;
  undefined local_1548;
  undefined4 local_1544;
  undefined4 local_1538;
  undefined auStack_1530 [72];
  undefined auStack_14e8 [304];
  undefined4 local_13b8;
  undefined4 local_13ac;
  undefined local_13a4;
  undefined4 local_13a0;
  undefined4 local_1394;
  undefined local_138c;
  undefined4 local_1388;
  undefined4 local_137c;
  undefined local_1374;
  undefined4 local_1370;
  undefined4 local_1364;
  undefined local_135c;
  undefined4 local_1358;
  undefined4 local_134c;
  undefined4 local_1344;
  undefined4 local_1340;
  undefined4 local_1334;
  undefined4 local_132c;
  undefined4 local_1328;
  undefined4 local_131c;
  undefined4 local_1314;
  undefined4 local_1310;
  undefined4 local_1304;
  undefined4 local_12fc;
  undefined4 local_12f8;
  undefined4 local_12ec;
  undefined local_12e4;
  undefined4 local_12e0;
  undefined4 local_12d4;
  undefined auStack_12cc [72];
  undefined auStack_1284 [304];
  undefined4 local_1154;
  undefined4 local_1148;
  undefined local_1140;
  undefined4 local_113c;
  undefined4 local_1130;
  undefined local_1128;
  undefined4 local_1124;
  undefined4 local_1118;
  undefined local_1110;
  undefined4 local_110c;
  undefined4 local_1100;
  undefined local_10f8;
  undefined4 local_10f4;
  undefined4 local_10e8;
  undefined4 local_10e0;
  undefined4 local_10dc;
  undefined4 local_10d0;
  undefined4 local_10c8;
  undefined4 local_10c4;
  undefined4 local_10b8;
  undefined4 local_10b0;
  undefined4 local_10ac;
  undefined4 local_10a0;
  undefined4 local_1098;
  undefined4 local_1094;
  undefined4 local_1088;
  undefined local_1080;
  undefined4 local_107c;
  undefined4 local_1070;
  undefined4 local_1068;
  undefined4 local_1064;
  undefined4 local_1058;
  undefined4 local_1050;
  undefined4 local_104c;
  undefined4 local_1040;
  undefined4 local_1038;
  undefined4 local_1034;
  undefined4 local_1028;
  undefined2 local_1020;
  undefined4 local_101c;
  undefined4 local_1010;
  undefined4 local_1008;
  undefined4 local_1004;
  undefined4 local_ff8;
  undefined4 local_ff0;
  undefined4 local_fec;
  undefined4 local_fe0;
  undefined local_fd8;
  undefined4 local_fd4;
  undefined4 local_fc8;
  undefined auStack_fc0 [256];
  undefined4 local_ec0;
  undefined4 local_eb4;
  undefined auStack_eac [256];
  undefined4 local_dac;
  undefined4 local_da0;
  undefined auStack_d98 [256];
  undefined4 local_c98;
  undefined4 local_c8c;
  undefined4 local_c84;
  undefined4 local_c80;
  undefined4 local_c74;
  undefined4 local_c6c;
  undefined4 local_c68;
  undefined4 local_c64;
  undefined4 local_c60;
  undefined4 local_c5c;
  undefined4 local_c50;
  undefined4 local_c48;
  undefined4 local_c44;
  undefined4 local_c38;
  undefined4 local_c30;
  undefined4 local_c2c;
  undefined4 local_c20;
  undefined4 local_c18;
  undefined4 local_c14;
  undefined4 local_c08;
  undefined4 local_c00;
  undefined4 local_bfc;
  undefined4 local_bf0;
  undefined local_be8;
  undefined4 local_be4;
  undefined4 local_bd8;
  undefined local_bd0;
  undefined4 local_bcc;
  undefined4 local_bc0;
  undefined local_bb8;
  undefined4 local_bb4;
  undefined4 local_ba8;
  undefined4 local_ba0;
  undefined4 local_b9c;
  undefined4 local_b90;
  undefined4 local_b88;
  undefined4 local_b84;
  undefined4 local_b78;
  undefined local_b70;
  undefined4 local_b6c;
  undefined4 local_b60;
  undefined local_b58;
  undefined4 local_b54;
  undefined4 local_b48;
  undefined auStack_b40 [72];
  undefined auStack_af8 [304];
  undefined4 local_9c8;
  undefined4 local_9bc;
  undefined local_9b4;
  undefined4 local_9b0;
  undefined4 local_9a4;
  undefined local_99c;
  undefined4 local_998;
  undefined4 local_98c;
  undefined local_984;
  undefined4 local_980;
  undefined4 local_974;
  undefined local_96c;
  undefined4 local_968;
  undefined4 local_95c;
  undefined4 local_954;
  undefined4 local_950;
  undefined4 local_944;
  undefined4 local_93c;
  undefined4 local_938;
  undefined4 local_92c;
  undefined4 local_924;
  undefined4 local_920;
  undefined4 local_914;
  undefined4 local_90c;
  undefined4 local_908;
  undefined4 local_8fc;
  undefined local_8f4;
  undefined4 local_8f0;
  undefined4 local_8e4;
  undefined auStack_8dc [72];
  undefined auStack_894 [304];
  undefined4 local_764;
  undefined4 local_758;
  undefined local_750;
  undefined4 local_74c;
  undefined4 local_740;
  undefined local_738;
  undefined4 local_734;
  undefined4 local_728;
  undefined local_720;
  undefined4 local_71c;
  undefined4 local_710;
  undefined local_708;
  undefined4 local_704;
  undefined4 local_6f8;
  undefined4 local_6f0;
  undefined4 local_6ec;
  undefined4 local_6e0;
  undefined4 local_6d8;
  undefined4 local_6d4;
  undefined4 local_6c8;
  undefined4 local_6c0;
  undefined4 local_6bc;
  undefined4 local_6b0;
  undefined4 local_6a8;
  undefined4 local_6a4;
  undefined4 local_698;
  undefined local_690;
  undefined4 local_68c;
  undefined4 local_680;
  undefined4 local_678;
  undefined4 local_674;
  undefined4 local_668;
  undefined4 local_660;
  undefined4 local_65c;
  undefined4 local_650;
  undefined4 local_648;
  undefined4 local_644;
  undefined4 local_638;
  undefined2 local_630;
  undefined4 local_62c;
  undefined4 local_620;
  undefined4 local_618;
  undefined4 local_614;
  undefined4 local_608;
  undefined4 local_600;
  undefined4 local_5fc;
  undefined4 local_5f0;
  undefined local_5e8;
  undefined4 local_5e4;
  undefined4 local_5d8;
  undefined auStack_5d0 [256];
  undefined4 local_4d0;
  undefined4 local_4c4;
  undefined auStack_4bc [256];
  undefined4 local_3bc;
  undefined4 local_3b0;
  undefined auStack_3a8 [256];
  undefined4 local_2a8;
  undefined4 local_29c;
  undefined4 local_294;
  undefined4 local_290;
  undefined4 local_284;
  undefined4 local_27c;
  undefined4 local_278;
  undefined4 local_274;
  undefined4 local_270;
  undefined4 local_26c;
  undefined4 local_260;
  undefined4 local_258;
  undefined4 local_254;
  undefined4 local_248;
  undefined4 local_240;
  undefined4 local_23c;
  undefined4 local_230;
  undefined4 local_228;
  undefined4 local_224;
  undefined4 local_218;
  undefined4 local_210;
  undefined4 local_20c;
  undefined4 local_200;
  undefined local_1f8;
  undefined4 local_1f4;
  undefined4 local_1e8;
  undefined local_1e0;
  undefined4 local_1dc;
  undefined4 local_1d0;
  undefined local_1c8;
  undefined4 local_1c4;
  undefined4 local_1b8;
  undefined4 local_1b0;
  undefined4 local_1ac;
  undefined4 local_1a0;
  undefined4 local_198;
  undefined4 local_194;
  undefined auStack_190 [8];
  code *local_188;
  code *local_184;
  byte local_180;
  undefined4 local_17c;
  undefined auStack_178 [8];
  code *local_170;
  undefined local_168;
  undefined4 local_164;
  undefined auStack_160 [8];
  code *local_158;
  undefined local_150;
  undefined auStack_14c [8];
  code *local_144;
  undefined4 local_13c;
  undefined local_138;
  undefined4 local_134;
  undefined auStack_130 [8];
  code *local_128;
  undefined4 local_120;
  undefined4 local_11c;
  undefined auStack_118 [8];
  code *local_110;
  undefined4 local_108;
  undefined4 local_104;
  undefined auStack_100 [8];
  code *local_f8;
  undefined local_f0;
  undefined4 local_ec;
  undefined auStack_e8 [8];
  code *local_e0;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined auStack_d0 [8];
  code *local_c8;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined auStack_b8 [8];
  code *local_b0;
  undefined4 local_a8;
  undefined auStack_a4 [8];
  code *local_9c;
  undefined4 local_94;
  undefined2 local_90;
  undefined local_8e;
  undefined4 local_8c;
  undefined auStack_88 [8];
  code *local_80;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined auStack_64 [8];
  code *local_5c;
  undefined4 local_54;
  undefined4 local_50;
  undefined auStack_4c [8];
  code *local_44;
  undefined4 local_3c;
  undefined4 uStack_38;
  
  uVar2 = DAT_08024b94;
  puVar1 = DAT_08024b90;
  if (*DAT_08024b8c == 3) {
    return 1;
  }
  if (0x2f < param_1) {
    return 9;
  }
  *DAT_08024b8c = 1;
  FUN_0804cb58(uVar2);
  if (*puVar1 != param_1) {
    FUN_080569f8(DAT_08024b9c,DAT_08024b98,param_1 + 1);
    uVar3 = DAT_08024ba0;
    uVar2 = DAT_08024b9c;
    *puVar1 = param_1;
    FUN_0804cb68(uVar3,uVar2);
    FUN_08051058(DAT_08024ba8,DAT_08024ba4,1);
    bVar8 = FUN_0805253c(DAT_08024b9c);
    if ((bVar8 & 0xf7) == 0) {
      bVar8 = FUN_0801f448();
    }
    if (bVar8 != 0) {
      if (bVar8 != 1) {
        if (bVar8 == 0x12) {
          iVar9 = 2;
        }
        else {
          iVar9 = 0;
        }
        *DAT_08024b8c = iVar9;
        return bVar8;
      }
      *DAT_080265b4 = 3;
      return 1;
    }
  }
  uVar4 = DAT_08024f54;
  uVar3 = DAT_08024f50;
  uVar2 = DAT_08024f4c;
  local_5108 = 0;
  local_5100 = 0;
  local_50f0 = 0;
  puVar10 = (undefined4 *)((int)&uStack_38 + DAT_08024f48);
  local_50e8 = 0;
  local_50d8 = 0;
  local_50e4 = DAT_08024f50;
  local_5114[0] = DAT_08024f4c;
  local_50fc = DAT_08024f4c;
  FUN_08056428(auStack_50d0,0,0x48);
  uVar6 = DAT_08024f8c;
  FUN_08016170(auStack_5088);
  uVar7 = DAT_08024f90;
  uVar5 = DAT_08024f58;
  local_4f4c = 0;
  local_4f44 = 0;
  local_4f34 = 0;
  local_4f2c = 0;
  local_4f1c = 0;
  local_4f14 = 0;
  local_4f04 = 0;
  local_4efc = 0;
  local_4eec = 0;
  local_4ed4 = 0;
  local_4ebc = 0;
  local_4ea4 = 0;
  local_4e8c = 0;
  local_4e84 = 0;
  local_4e80 = uVar3;
  local_4e74 = 0;
  local_4f58 = uVar2;
  local_4f40 = uVar2;
  local_4f28 = uVar2;
  local_4f10 = uVar2;
  local_4ef8 = uVar4;
  local_4ee4 = 0;
  uStack_4ee0 = uVar4;
  local_4ecc = 0;
  uStack_4ec8 = uVar4;
  local_4eb4 = 0;
  uStack_4eb0 = uVar4;
  local_4e9c = 0;
  uStack_4e98 = uVar2;
  FUN_08056428(auStack_4e6c,0,0x48);
  FUN_08016170(auStack_4e24);
  local_4ce8 = 0;
  local_4ce0 = 0;
  local_4cd0 = 0;
  local_4cc8 = 0;
  local_4cb8 = 0;
  local_4cb0 = 0;
  local_4ca0 = 0;
  local_4c98 = 0;
  local_4c88 = 0;
  local_4c80 = 0;
  local_4c70 = 0;
  local_4c68 = 0;
  local_4c58 = 0;
  local_4c50 = 0;
  local_4c40 = 0;
  local_4c38 = 0;
  local_4c28 = 0;
  local_4c20 = 0;
  local_4c10 = 0;
  local_4bf8 = 0;
  local_4c08 = 0x1000000;
  local_4c1c = DAT_08024f60;
  local_4c04 = DAT_08024f64;
  local_4cf4 = uVar2;
  local_4cdc = uVar2;
  local_4cc4 = uVar2;
  local_4cac = uVar2;
  local_4c94 = uVar4;
  local_4c7c = uVar4;
  local_4c64 = uVar4;
  local_4c4c = uVar4;
  local_4c34 = uVar2;
  local_4bf0 = uVar6;
  local_4bbc = DAT_08024f5c;
  local_4ba4 = DAT_08024f5c;
  local_4bec = DAT_08024f68;
  local_4b90 = uVar5;
  local_4bd4 = DAT_08024f6c;
  local_4b8c = DAT_08024f70;
  local_4ba8 = uVar5;
  local_4be0 = 0;
  local_4bd8 = uVar6;
  local_4bc8 = 0;
  local_4bc0 = 0;
  local_4bb0 = 0;
  local_4b98 = 0;
  local_4b80 = 0;
  local_4b78 = 0;
  local_4b74 = uVar7;
  local_4b68 = 0;
  FUN_08056428(auStack_4b60,0,0x100);
  local_4a60 = uVar7;
  local_4a54 = 0;
  FUN_08056428(auStack_4a4c,0,0x100);
  local_494c = uVar7;
  local_4940 = 0;
  FUN_08056428(auStack_4938,0,0x100);
  local_4820 = DAT_08024f74;
  local_4838 = DAT_08024f78;
  local_47fc = DAT_08024f7c;
  local_47cc = DAT_08024f80;
  local_47e4 = DAT_08024f84;
  local_47b4 = DAT_08024f88;
  local_4808 = uVar5;
  local_4800 = 0x3f800000;
  local_4804 = 0xbf800000;
  local_482c = 0;
  local_4824 = 0x1000000;
  local_4814 = 0;
  local_47f0 = 0;
  local_47e8 = 0x1000000;
  local_47d8 = 0;
  local_47d0 = 0x1000000;
  local_47c0 = 0;
  local_47b8 = 0x1000000;
  local_47a8 = 0;
  local_47a0 = uVar6;
  local_4790 = 0;
  local_4788 = 0;
  local_4778 = 0;
  local_4770 = 0;
  local_4760 = 0;
  local_4758 = 0;
  local_4748 = 0;
  local_480c = uVar5;
  local_479c = uVar2;
  local_4784 = uVar2;
  local_476c = uVar2;
  local_4754 = uVar4;
  local_4740 = 0;
  local_4730 = 0;
  local_4728 = 0;
  local_4718 = 0;
  local_4710 = 0;
  local_4700 = 0;
  local_46f8 = 0;
  local_46f4 = uVar3;
  local_46e8 = 0;
  local_473c = uVar4;
  local_4724 = uVar2;
  local_470c = uVar2;
  FUN_08056428(auStack_46e0,0,0x48);
  FUN_08016170(auStack_4698);
  local_455c = 0;
  local_4554 = 0;
  local_4544 = 0;
  local_453c = 0;
  local_452c = 0;
  local_4524 = 0;
  local_4514 = 0;
  local_450c = 0;
  local_44fc = 0;
  local_44f4 = 0;
  local_44e4 = 0;
  local_44dc = 0;
  local_44cc = 0;
  local_44c4 = 0;
  local_44b4 = 0;
  local_44ac = 0;
  local_449c = 0;
  local_4494 = 0;
  local_4490 = uVar3;
  local_4484 = 0;
  local_4568 = uVar2;
  local_4550 = uVar2;
  local_4538 = uVar2;
  local_4520 = uVar2;
  local_4508 = uVar4;
  local_44f0 = uVar4;
  local_44d8 = uVar4;
  local_44c0 = uVar4;
  local_44a8 = uVar2;
  FUN_08056428(auStack_447c,0,0x48);
  uVar3 = DAT_08024f60;
  FUN_08016170(auStack_4434);
  local_42f8 = 0;
  local_42f0 = 0;
  local_42e0 = 0;
  local_42d8 = 0;
  local_42c8 = 0;
  local_42c0 = 0;
  local_42b0 = 0;
  local_42a8 = 0;
  local_4298 = 0;
  local_4290 = 0;
  local_4280 = 0;
  local_4278 = 0;
  local_4268 = 0;
  local_4260 = 0;
  local_4250 = 0;
  local_4248 = 0;
  local_4238 = 0;
  local_4230 = 0;
  local_422c = uVar3;
  local_4220 = 0;
  local_4218 = 0x1000000;
  local_4214 = DAT_08024f64;
  local_4208 = 0;
  local_4304 = uVar2;
  local_42ec = uVar2;
  local_42d4 = uVar2;
  local_42bc = uVar2;
  local_42a4 = uVar4;
  local_428c = uVar4;
  local_4274 = uVar4;
  local_425c = uVar4;
  local_4244 = uVar2;
  local_4200 = uVar6;
  local_41fc = DAT_08024f68;
  local_41cc = DAT_08024f5c;
  local_41b4 = DAT_08024f5c;
  local_419c = DAT_08024f70;
  local_41b8 = uVar5;
  local_41a0 = uVar5;
  local_41f0 = 0;
  local_41e8 = uVar6;
  local_41e4 = DAT_0802539c;
  local_41d8 = 0;
  local_41d0 = 0;
  local_41c0 = 0;
  local_41a8 = 0;
  local_4190 = 0;
  local_4188 = 0;
  local_4184 = uVar7;
  local_4178 = 0;
  FUN_08056428(auStack_4170,0,0x100);
  local_4070 = uVar7;
  local_4064 = 0;
  FUN_08056428(auStack_405c,0,0x100);
  local_3f5c = uVar7;
  local_3f50 = 0;
  FUN_08056428(auStack_3f48,0,0x100);
  local_3e48 = DAT_080253a0;
  local_3e30 = DAT_080253a4;
  local_3e0c = DAT_080253a8;
  local_3dc4 = DAT_080253ac;
  local_3e3c = 0;
  local_3e34 = 0x1000000;
  local_3e24 = 0;
  local_3e00 = 0;
  local_3df8 = 0x1000000;
  local_3df4 = DAT_080253b0;
  local_3de8 = 0;
  local_3de0 = 0x1000000;
  local_3ddc = DAT_080253b4;
  local_3dd0 = 0;
  local_3dc8 = 0x1000000;
  local_3db8 = 0;
  local_3da0 = 0;
  local_3d98 = 0;
  local_3d88 = 0;
  local_3d80 = 0;
  local_3d70 = 0;
  local_3d68 = 0;
  local_3d58 = 0;
  local_3e1c = uVar5;
  local_3e18 = uVar5;
  local_3e14 = 0xbf800000;
  local_3e10 = 0x3f800000;
  local_3d94 = uVar2;
  local_3d7c = uVar2;
  local_3d64 = uVar4;
  local_3db0 = uVar6;
  uStack_3dac = uVar2;
  local_3d50 = 0;
  uStack_3d4c = uVar4;
  local_3d40 = 0;
  local_3d28 = 0;
  local_3d20 = 0;
  local_3d10 = 0;
  local_3d08 = 0;
  local_3d04 = DAT_080253b8;
  local_3cf8 = 0;
  local_3d1c = uVar2;
  local_3d38 = 0;
  uStack_3d34 = uVar2;
  FUN_08056428(auStack_3cf0,0,0x48);
  FUN_08016170(auStack_3ca8);
  local_3b6c = 0;
  local_3b64 = 0;
  local_3b54 = 0;
  local_3b4c = 0;
  local_3b3c = 0;
  local_3b34 = 0;
  local_3b24 = 0;
  local_3b1c = 0;
  local_3b0c = 0;
  local_3b04 = 0;
  local_3af4 = 0;
  local_3aec = 0;
  local_3adc = 0;
  local_3ad4 = 0;
  local_3ac4 = 0;
  local_3abc = 0;
  local_3aac = 0;
  local_3aa4 = 0;
  local_3aa0 = DAT_080253b8;
  local_3a94 = 0;
  local_3b78 = uVar2;
  local_3b60 = uVar2;
  local_3b48 = uVar2;
  local_3b30 = uVar2;
  local_3b18 = uVar4;
  local_3b00 = uVar4;
  local_3ae8 = uVar4;
  local_3ad0 = uVar4;
  local_3ab8 = uVar2;
  FUN_08056428(auStack_3a8c,0,0x48);
  FUN_08016170(auStack_3a44);
  local_3908 = 0;
  local_3900 = 0;
  local_38f0 = 0;
  local_38e8 = 0;
  local_38d8 = 0;
  local_38d0 = 0;
  local_38c0 = 0;
  local_38b8 = 0;
  local_38a8 = 0;
  local_38a0 = 0;
  local_3890 = 0;
  local_3888 = 0;
  local_3878 = 0;
  local_3870 = 0;
  local_3860 = 0;
  local_3858 = 0;
  local_3848 = 0;
  local_3840 = 0;
  local_383c = DAT_080253bc;
  local_3830 = 0;
  local_3828 = 0x1000000;
  local_3824 = DAT_080253c0;
  local_3818 = 0;
  local_3914 = uVar2;
  local_38fc = uVar2;
  local_38e4 = uVar2;
  local_38cc = uVar2;
  local_38b4 = uVar4;
  local_389c = uVar4;
  local_3884 = uVar4;
  local_386c = uVar4;
  local_3854 = uVar2;
  local_3810 = uVar6;
  local_380c = DAT_080253c4;
  local_37ac = DAT_080253cc;
  local_3800 = 0;
  local_37f8 = uVar6;
  local_37f4 = DAT_0802539c;
  local_37e8 = 0;
  local_37e0 = 0;
  local_37dc = DAT_080253c8;
  local_37d0 = 0;
  local_37c4 = DAT_080253c8;
  local_37b8 = 0;
  local_37a0 = 0;
  local_3798 = 0;
  local_3794 = uVar7;
  local_3788 = 0;
  local_37c8 = uVar5;
  local_37b0 = uVar5;
  FUN_08056428(auStack_3780,0,0x100);
  local_3680 = uVar7;
  local_3674 = 0;
  FUN_08056428(auStack_366c,0,0x100);
  local_356c = uVar7;
  local_3560 = 0;
  FUN_08056428(auStack_3558,0,0x100);
  local_3458 = DAT_080253a0;
  local_3440 = DAT_080253a4;
  local_341c = DAT_080253a8;
  local_3404 = DAT_080253b0;
  local_33ec = DAT_080253b4;
  local_33d4 = DAT_080253ac;
  local_344c = 0;
  local_3444 = 0x1000000;
  local_3434 = 0;
  local_3410 = 0;
  local_3408 = 0x1000000;
  local_33f8 = 0;
  local_33f0 = 0x1000000;
  local_33e0 = 0;
  local_33d8 = 0x1000000;
  local_33c8 = 0;
  local_33c0 = uVar6;
  local_33b0 = 0;
  local_33a8 = 0;
  local_3398 = 0;
  local_3390 = 0;
  local_3380 = 0;
  local_3378 = 0;
  local_3368 = 0;
  local_3428 = uVar5;
  local_33bc = uVar2;
  local_33a4 = uVar2;
  local_338c = uVar2;
  local_3374 = uVar4;
  local_342c = uVar5;
  local_3424 = 0xbf800000;
  local_3420 = 0x3f800000;
  local_3360 = 0;
  local_3350 = 0;
  local_3348 = 0;
  local_3338 = 0;
  local_3330 = 0;
  local_3320 = 0;
  local_3318 = 0;
  local_3314 = DAT_080253b8;
  local_3308 = 0;
  local_335c = uVar4;
  local_3344 = uVar2;
  local_332c = uVar2;
  FUN_08056428(auStack_3300,0,0x48);
  FUN_08016170(auStack_32b8);
  local_317c = 0;
  local_3174 = 0;
  local_3164 = 0;
  local_315c = 0;
  local_314c = 0;
  local_3144 = 0;
  local_3134 = 0;
  local_312c = 0;
  local_311c = 0;
  local_3114 = 0;
  local_3104 = 0;
  local_30fc = 0;
  local_30ec = 0;
  local_30e4 = 0;
  local_30d4 = 0;
  local_30cc = 0;
  local_30bc = 0;
  local_30b4 = 0;
  local_30b0 = DAT_080257bc;
  local_30a4 = 0;
  local_3188 = uVar2;
  local_3170 = uVar2;
  local_3158 = uVar2;
  local_3140 = uVar2;
  local_3128 = uVar4;
  local_3110 = uVar4;
  local_30f8 = uVar4;
  local_30e0 = uVar4;
  local_30c8 = uVar2;
  FUN_08056428(auStack_309c,0,0x48);
  FUN_08016170(auStack_3054);
  local_2e4c = DAT_080257c0;
  local_2e34 = DAT_080257c4;
  local_2f18 = 0;
  local_2f10 = 0;
  local_2f00 = 0;
  local_2ef8 = 0;
  local_2ee8 = 0;
  local_2ee0 = 0;
  local_2ed0 = 0;
  local_2ec8 = 0;
  local_2eb8 = 0;
  local_2ea0 = 0;
  local_2e88 = 0;
  local_2e70 = 0;
  local_2e58 = 0;
  local_2e50 = 0;
  local_2e40 = 0;
  local_2e38 = 0x1000000;
  local_2e28 = 0;
  local_2f24 = uVar2;
  local_2f0c = uVar2;
  local_2ef4 = uVar2;
  local_2edc = uVar2;
  local_2ec4 = uVar4;
  local_2eb0 = 0;
  uStack_2eac = uVar4;
  local_2e98 = 0;
  uStack_2e94 = uVar4;
  local_2e80 = 0;
  uStack_2e7c = uVar4;
  local_2e68 = 0;
  uStack_2e64 = uVar2;
  local_2e20 = uVar6;
  local_2e1c = DAT_080257c8;
  local_2e10 = 0;
  local_2e08 = uVar6;
  local_2e04 = DAT_080257d0;
  local_2df8 = 0;
  local_2df0 = 0;
  local_2dec = DAT_080257cc;
  local_2de0 = 0;
  local_2dd4 = DAT_080257cc;
  local_2dc8 = 0;
  local_2dbc = DAT_080257d4;
  local_2db0 = 0;
  local_2da8 = 0;
  local_2da4 = uVar7;
  local_2d98 = 0;
  local_2dd8 = uVar5;
  local_2dc0 = uVar5;
  FUN_08056428(auStack_2d90,0,0x100);
  local_2c90 = uVar7;
  local_2c84 = 0;
  FUN_08056428(auStack_2c7c,0,0x100);
  local_2b7c = uVar7;
  local_2b70 = 0;
  FUN_08056428(auStack_2b68,0,0x100);
  local_2a68 = DAT_080257d8;
  local_2a50 = DAT_080257dc;
  local_2a2c = DAT_080257e0;
  local_2a14 = DAT_080257e4;
  local_29fc = DAT_080257e8;
  local_29e4 = DAT_080257ec;
  local_2a34 = 0xbf800000;
  local_2a5c = 0;
  local_2a54 = 0x1000000;
  local_2a44 = 0;
  local_2a20 = 0;
  local_2a18 = 0x1000000;
  local_2a08 = 0;
  local_2a00 = 0x1000000;
  local_29f0 = 0;
  local_29e8 = 0x1000000;
  local_29d8 = 0;
  local_29d0 = uVar6;
  local_29c0 = 0;
  local_29b8 = 0;
  local_29a8 = 0;
  local_29a0 = 0;
  local_2990 = 0;
  local_2988 = 0;
  local_2978 = 0;
  local_29cc = uVar2;
  local_29b4 = uVar2;
  local_299c = uVar2;
  local_2984 = uVar4;
  local_2a3c = uVar5;
  local_2a38 = uVar5;
  local_2a30 = 0x3f800000;
  local_2970 = 0;
  local_2960 = 0;
  local_2958 = 0;
  local_2948 = 0;
  local_2940 = 0;
  local_2930 = 0;
  local_2928 = 0;
  local_2924 = DAT_080257bc;
  local_2918 = 0;
  local_296c = uVar4;
  local_2954 = uVar2;
  local_293c = uVar2;
  FUN_08056428(auStack_2910,0,0x48);
  FUN_08016170(auStack_28c8);
  local_278c = 0;
  local_2784 = 0;
  local_2774 = 0;
  local_276c = 0;
  local_275c = 0;
  local_2754 = 0;
  local_2744 = 0;
  local_273c = 0;
  local_272c = 0;
  local_2724 = 0;
  local_2714 = 0;
  local_270c = 0;
  local_26fc = 0;
  local_26f4 = 0;
  local_26e4 = 0;
  local_26dc = 0;
  local_26cc = 0;
  local_26c4 = 0;
  local_26c0 = DAT_080257bc;
  local_26b4 = 0;
  local_2798 = uVar2;
  local_2780 = uVar2;
  local_2768 = uVar2;
  local_2750 = uVar2;
  local_2738 = uVar4;
  local_2720 = uVar4;
  local_2708 = uVar4;
  local_26f0 = uVar4;
  local_26d8 = uVar2;
  FUN_08056428(auStack_26ac,0,0x48);
  FUN_08016170(auStack_2664);
  local_2528 = 0;
  local_2520 = 0;
  local_2510 = 0;
  local_2508 = 0;
  local_24f8 = 0;
  local_24f0 = 0;
  local_24e0 = 0;
  local_24d8 = 0;
  local_24c8 = 0;
  local_24c0 = 0;
  local_24b0 = 0;
  local_24a8 = 0;
  local_2498 = 0;
  local_2490 = 0;
  local_2480 = 0;
  local_2478 = 0;
  local_2468 = 0;
  local_2460 = 0;
  local_245c = DAT_080257c0;
  local_2450 = 0;
  local_2448 = 0x1000000;
  local_2444 = DAT_080257c4;
  local_2438 = 0;
  local_2534 = uVar2;
  local_251c = uVar2;
  local_2504 = uVar2;
  local_24ec = uVar2;
  local_24d4 = uVar4;
  local_24bc = uVar4;
  local_24a4 = uVar4;
  local_248c = uVar4;
  local_2474 = uVar2;
  local_2430 = uVar6;
  local_242c = DAT_080257c8;
  local_23fc = DAT_080257cc;
  local_23e4 = DAT_080257cc;
  local_2420 = 0;
  local_2418 = uVar6;
  local_2414 = DAT_080257d0;
  local_2408 = 0;
  local_2400 = 0;
  local_23f0 = 0;
  local_23d8 = 0;
  local_23cc = DAT_080257d4;
  local_23c0 = 0;
  local_23b8 = 0;
  local_23b4 = uVar7;
  local_23a8 = 0;
  local_23e8 = uVar5;
  local_23d0 = uVar5;
  FUN_08056428(auStack_23a0,0,0x100);
  local_22a0 = uVar7;
  local_2294 = 0;
  FUN_08056428(auStack_228c,0,0x100);
  local_218c = uVar7;
  local_2180 = 0;
  FUN_08056428(auStack_2178,0,0x100);
  uVar3 = DAT_08025c40;
  local_2078 = DAT_08025c28;
  local_2060 = DAT_08025c2c;
  local_206c = 0;
  local_2064 = 0x1000000;
  local_2054 = 0;
  local_203c = DAT_08025c30;
  local_2024 = DAT_08025c34;
  local_200c = DAT_08025c38;
  local_1ff4 = DAT_08025c3c;
  local_2048 = uVar5;
  local_2030 = 0;
  local_2028 = 0x1000000;
  local_2018 = 0;
  local_2010 = 0x1000000;
  local_2000 = 0;
  local_1ff8 = 0x1000000;
  local_1fe8 = 0;
  local_1fd0 = 0;
  local_1fc8 = 0;
  local_1fb8 = 0;
  local_1fb0 = 0;
  local_1fa0 = 0;
  local_1f98 = 0;
  local_1f88 = 0;
  local_1fc4 = uVar2;
  local_1fac = uVar2;
  local_1f94 = uVar4;
  local_204c = uVar5;
  local_2044 = 0xbf800000;
  local_2040 = 0x3f800000;
  local_1fe0 = uVar6;
  uStack_1fdc = uVar2;
  local_1f80 = 0;
  uStack_1f7c = uVar4;
  local_1f70 = 0;
  local_1f58 = 0;
  local_1f50 = 0;
  local_1f40 = 0;
  local_1f38 = 0;
  local_1f34 = DAT_08025c40;
  local_1f28 = 0;
  local_1f4c = uVar2;
  local_1f68 = 0;
  uStack_1f64 = uVar2;
  FUN_08056428(auStack_1f20,0,0x48);
  FUN_08016170(auStack_1ed8);
  local_1d9c = 0;
  local_1d94 = 0;
  local_1d84 = 0;
  local_1d7c = 0;
  local_1d6c = 0;
  local_1d64 = 0;
  local_1d54 = 0;
  local_1d4c = 0;
  local_1d3c = 0;
  local_1d24 = 0;
  local_1d0c = 0;
  local_1cf4 = 0;
  local_1cdc = 0;
  local_1cd4 = 0;
  local_1cd0 = uVar3;
  local_1cc4 = 0;
  local_1da8 = uVar2;
  local_1d90 = uVar2;
  local_1d78 = uVar2;
  local_1d60 = uVar2;
  local_1d48 = uVar4;
  local_1d34 = 0;
  uStack_1d30 = uVar4;
  local_1d1c = 0;
  uStack_1d18 = uVar4;
  local_1d04 = 0;
  uStack_1d00 = uVar4;
  local_1cec = 0;
  uStack_1ce8 = uVar2;
  FUN_08056428(auStack_1cbc,0,0x48);
  FUN_08016170(auStack_1c74);
  local_1b38 = 0;
  local_1b30 = 0;
  local_1b20 = 0;
  local_1b18 = 0;
  local_1b08 = 0;
  local_1b00 = 0;
  local_1af0 = 0;
  local_1ae8 = 0;
  local_1ad8 = 0;
  local_1ad0 = 0;
  local_1ac0 = 0;
  local_1ab8 = 0;
  local_1aa8 = 0;
  local_1aa0 = 0;
  local_1a90 = 0;
  local_1a88 = 0;
  local_1a78 = 0;
  local_1a70 = 0;
  local_1a6c = DAT_08025c44;
  local_1a60 = 0;
  local_1a58 = 0x1000000;
  local_1a54 = DAT_08025c48;
  local_1a48 = 0;
  local_1b44 = uVar2;
  local_1b2c = uVar2;
  local_1b14 = uVar2;
  local_1afc = uVar2;
  local_1ae4 = uVar4;
  local_1acc = uVar4;
  local_1ab4 = uVar4;
  local_1a9c = uVar4;
  local_1a84 = uVar2;
  local_1a40 = uVar6;
  local_1a3c = DAT_08025c4c;
  local_1a24 = DAT_08025c54;
  local_1a0c = DAT_08025c50;
  local_19f4 = DAT_08025c50;
  local_19e0 = uVar5;
  local_1a30 = 0;
  local_1a28 = uVar6;
  local_1a18 = 0;
  local_1a10 = 0;
  local_1a00 = 0;
  local_19e8 = 0;
  local_19dc = DAT_08025c58;
  local_19d0 = 0;
  local_19c8 = 0;
  local_19c4 = uVar7;
  local_19b8 = 0;
  local_19f8 = uVar5;
  FUN_08056428(auStack_19b0,0,0x100);
  local_18b0 = uVar7;
  local_18a4 = 0;
  FUN_08056428(auStack_189c,0,0x100);
  local_179c = uVar7;
  local_1790 = 0;
  FUN_08056428(auStack_1788,0,0x100);
  local_1688 = DAT_08025c28;
  local_1670 = DAT_08025c2c;
  local_164c = DAT_08025c30;
  local_1634 = DAT_08025c34;
  local_161c = DAT_08025c38;
  local_1604 = DAT_08025c3c;
  local_165c = uVar5;
  local_167c = 0;
  local_1674 = 0x1000000;
  local_1664 = 0;
  local_1640 = 0;
  local_1638 = 0x1000000;
  local_1628 = 0;
  local_1620 = 0x1000000;
  local_1610 = 0;
  local_1608 = 0x1000000;
  local_15f8 = 0;
  local_15f0 = uVar6;
  local_15e0 = 0;
  local_15d8 = 0;
  local_15c8 = 0;
  local_15c0 = 0;
  local_15b0 = 0;
  local_15a8 = 0;
  local_1598 = 0;
  local_15ec = uVar2;
  local_15d4 = uVar2;
  local_15bc = uVar2;
  local_15a4 = uVar4;
  local_1658 = uVar5;
  local_1654 = 0xbf800000;
  local_1650 = 0x3f800000;
  local_1590 = 0;
  local_1580 = 0;
  local_1578 = 0;
  local_1568 = 0;
  local_1560 = 0;
  local_1550 = 0;
  local_1548 = 0;
  local_1544 = uVar3;
  local_1538 = 0;
  local_158c = uVar4;
  local_1574 = uVar2;
  local_155c = uVar2;
  FUN_08056428(auStack_1530,0,0x48);
  FUN_08016170(auStack_14e8);
  local_13ac = 0;
  local_13a4 = 0;
  local_1394 = 0;
  local_138c = 0;
  local_137c = 0;
  local_1374 = 0;
  local_1364 = 0;
  local_135c = 0;
  local_134c = 0;
  local_1344 = 0;
  local_1334 = 0;
  local_132c = 0;
  local_131c = 0;
  local_1314 = 0;
  local_1304 = 0;
  local_12fc = 0;
  local_12ec = 0;
  local_12e4 = 0;
  local_12e0 = uVar3;
  local_12d4 = 0;
  local_13b8 = uVar2;
  local_13a0 = uVar2;
  local_1388 = uVar2;
  local_1370 = uVar2;
  local_1358 = uVar4;
  local_1340 = uVar4;
  local_1328 = uVar4;
  local_1310 = uVar4;
  local_12f8 = uVar2;
  FUN_08056428(auStack_12cc,0,0x48);
  FUN_08016170(auStack_1284);
  local_107c = DAT_08026028;
  local_1148 = 0;
  local_1140 = 0;
  local_1130 = 0;
  local_1128 = 0;
  local_1118 = 0;
  local_1110 = 0;
  local_1100 = 0;
  local_10f8 = 0;
  local_10e8 = 0;
  local_10e0 = 0;
  local_10d0 = 0;
  local_10c8 = 0;
  local_10b0 = 0;
  local_10a0 = 0;
  local_1098 = 0;
  local_1088 = 0;
  local_1080 = 0;
  local_1070 = 0;
  local_1068 = 0x1000000;
  local_1064 = DAT_0802602c;
  local_1058 = 0;
  local_10b8 = 0;
  local_1154 = uVar2;
  local_113c = uVar2;
  local_1124 = uVar2;
  local_110c = uVar2;
  local_10f4 = uVar4;
  local_10dc = uVar4;
  local_10c4 = uVar4;
  local_10ac = uVar4;
  local_1094 = uVar2;
  local_1050 = uVar6;
  local_104c = DAT_08026030;
  local_1040 = 0;
  local_1038 = uVar6;
  local_1034 = DAT_08026038;
  local_1028 = 0;
  local_1020 = 0;
  local_101c = DAT_08026034;
  local_1010 = 0;
  local_1004 = DAT_08026034;
  local_ff8 = 0;
  local_fec = DAT_0802603c;
  local_fe0 = 0;
  local_fd8 = 0;
  local_fd4 = uVar7;
  local_fc8 = 0;
  local_1008 = uVar5;
  local_ff0 = uVar5;
  FUN_08056428(auStack_fc0,0,0x100);
  local_ec0 = uVar7;
  local_eb4 = 0;
  FUN_08056428(auStack_eac,0,0x100);
  local_dac = uVar7;
  local_da0 = 0;
  FUN_08056428(auStack_d98,0,0x100);
  local_c98 = DAT_08026040;
  local_c80 = DAT_08026044;
  local_c5c = DAT_08026048;
  local_c8c = 0;
  local_c84 = 0x1000000;
  local_c74 = 0;
  local_c50 = 0;
  local_c48 = 0x1000000;
  local_c44 = DAT_0802604c;
  local_c38 = 0;
  local_c30 = 0x1000000;
  local_c2c = DAT_08026050;
  local_c20 = 0;
  local_c18 = 0x1000000;
  local_c14 = DAT_08026054;
  local_c08 = 0;
  local_c00 = uVar6;
  local_bf0 = 0;
  local_be8 = 0;
  local_bd8 = 0;
  local_bd0 = 0;
  local_bc0 = 0;
  local_bb8 = 0;
  local_ba8 = 0;
  local_c6c = uVar5;
  local_c68 = uVar5;
  local_c64 = 0xbf800000;
  local_c60 = 0x3f800000;
  local_bfc = uVar2;
  local_be4 = uVar2;
  local_bcc = uVar2;
  local_bb4 = uVar4;
  local_ba0 = 0;
  local_b54 = DAT_08026058;
  local_b90 = 0;
  local_b88 = 0;
  local_b78 = 0;
  local_b70 = 0;
  local_b60 = 0;
  local_b58 = 0;
  local_b48 = 0;
  local_b9c = uVar4;
  local_b84 = uVar2;
  local_b6c = uVar2;
  FUN_08056428(auStack_b40,0,0x48);
  FUN_08016170(auStack_af8);
  local_9bc = 0;
  local_8f0 = DAT_08026058;
  local_9b4 = 0;
  local_9a4 = 0;
  local_99c = 0;
  local_98c = 0;
  local_984 = 0;
  local_974 = 0;
  local_96c = 0;
  local_95c = 0;
  local_954 = 0;
  local_944 = 0;
  local_93c = 0;
  local_92c = 0;
  local_924 = 0;
  local_914 = 0;
  local_90c = 0;
  local_8fc = 0;
  local_8f4 = 0;
  local_8e4 = 0;
  local_9c8 = uVar2;
  local_9b0 = uVar2;
  local_998 = uVar2;
  local_980 = uVar2;
  local_968 = uVar4;
  local_950 = uVar4;
  local_938 = uVar4;
  local_920 = uVar4;
  local_908 = uVar2;
  FUN_08056428(auStack_8dc,0,0x48);
  FUN_08016170(auStack_894);
  local_674 = DAT_0802602c;
  local_758 = 0;
  local_750 = 0;
  local_740 = 0;
  local_738 = 0;
  local_728 = 0;
  local_720 = 0;
  local_710 = 0;
  local_708 = 0;
  local_6f8 = 0;
  local_6f0 = 0;
  local_6e0 = 0;
  local_6d8 = 0;
  local_6c8 = 0;
  local_6c0 = 0;
  local_6b0 = 0;
  local_6a8 = 0;
  local_698 = 0;
  local_690 = 0;
  local_68c = DAT_08026028;
  local_680 = 0;
  local_678 = 0x1000000;
  local_668 = 0;
  local_764 = uVar2;
  local_74c = uVar2;
  local_734 = uVar2;
  local_71c = uVar2;
  local_704 = uVar4;
  local_6ec = uVar4;
  local_6d4 = uVar4;
  local_6bc = uVar4;
  local_6a4 = uVar2;
  local_660 = uVar6;
  local_65c = DAT_08026030;
  local_5fc = DAT_0802603c;
  local_644 = DAT_08026038;
  local_62c = DAT_08026034;
  local_614 = DAT_08026034;
  local_650 = 0;
  local_648 = uVar6;
  local_638 = 0;
  local_630 = 0;
  local_620 = 0;
  local_608 = 0;
  local_5f0 = 0;
  local_5e8 = 0;
  local_5e4 = uVar7;
  local_5d8 = 0;
  local_618 = uVar5;
  local_600 = uVar5;
  FUN_08056428(auStack_5d0,0,0x100);
  local_4d0 = uVar7;
  local_4c4 = 0;
  FUN_08056428(auStack_4bc,0,0x100);
  local_3bc = uVar7;
  local_3b0 = 0;
  FUN_08056428(auStack_3a8,0,0x100);
  local_2a8 = DAT_08026040;
  local_26c = DAT_08026048;
  local_224 = DAT_080263a4;
  local_210 = uVar6;
  local_254 = DAT_080263a8;
  local_27c = uVar5;
  local_23c = DAT_080263ac;
  local_278 = uVar5;
  local_274 = 0xbf800000;
  local_29c = 0;
  local_294 = 0x1000000;
  local_290 = DAT_080263b0;
  local_284 = 0;
  local_260 = 0;
  local_258 = 0x1000000;
  local_248 = 0;
  local_240 = 0x1000000;
  local_230 = 0;
  local_228 = 0x1000000;
  local_218 = 0;
  local_200 = 0;
  local_1f8 = 0;
  local_1e8 = 0;
  local_1e0 = 0;
  local_1d0 = 0;
  local_1c8 = 0;
  local_1b8 = 0;
  local_270 = 0x3f800000;
  local_20c = uVar2;
  local_1f4 = uVar2;
  local_1dc = uVar2;
  local_1c4 = uVar4;
  local_1b0 = 0;
  local_ec = DAT_080263b4;
  local_138 = 8;
  local_134 = DAT_080263b8;
  local_1a0 = 0;
  local_198 = 0;
  local_188 = (code *)0x0;
  local_180 = 0;
  local_170 = (code *)0x0;
  local_168 = 0;
  local_158 = (code *)0x0;
  local_150 = 0;
  local_144 = (code *)0x0;
  local_13c = 0;
  local_128 = (code *)0x0;
  local_120 = 0x1000000;
  local_110 = (code *)0x0;
  local_108 = 0x1000000;
  local_f8 = (code *)0x0;
  local_f0 = 0;
  local_e0 = (code *)0x0;
  local_d8 = 0x1000000;
  local_c8 = (code *)0x0;
  local_c0 = 0x1000000;
  local_b0 = (code *)0x0;
  local_11c = DAT_080263bc;
  local_d4 = DAT_080263c0;
  local_bc = DAT_080263c4;
  local_1ac = uVar4;
  local_194 = uVar2;
  local_17c = uVar2;
  local_164 = uVar2;
  local_104 = uVar2;
  local_a8 = 0x1000000;
  local_8c = DAT_080263b0;
  local_94 = 0;
  local_78 = uVar5;
  local_9c = (code *)0x0;
  local_90 = 0;
  local_80 = (code *)0x0;
  local_5c = (code *)0x0;
  local_54 = 0;
  local_44 = (code *)0x0;
  local_3c = 0;
  local_5116 = '\0';
  local_74 = uVar5;
  local_70 = 0xff7fffff;
  local_6c = DAT_080263c8;
  local_68 = uVar4;
  local_50 = uVar4;
  local_8e = 0xff;
  FUN_0804cb58(DAT_080263cc);
  local_5117 = FUN_08024414(DAT_080263d0,local_5114);
  if (local_5117 == 0) {
    local_5117 = FUN_0801e104(puVar10,&local_5116);
    if (local_5117 == 0) {
      if (local_5116 != '\0') {
        if (*DAT_080265b4 == 3) {
          local_5117 = 1;
        }
        else {
          local_5117 = FUN_080216f8(DAT_080265b8,puVar10);
        }
      }
      iVar9 = DAT_080265d4;
      if (local_5117 == 0) {
        iVar16 = 1;
        uVar12 = 0;
        do {
          uVar14 = uVar12 >> 5;
          uVar13 = 1 << (uVar12 & 0x1f);
          if ((uVar13 & *(uint *)(iVar9 + uVar14 * 4)) != 0) {
            FUN_0804cb68(DAT_080265bc,iVar16);
            FUN_080569f8(DAT_080265c4,DAT_080265c0,iVar16);
            iVar11 = FUN_08024414(DAT_080265c4,puVar10);
            bVar8 = (byte)uVar12;
            if (((iVar11 == 0) && ((uint)local_180 != (uVar12 & 0xff))) &&
               (local_180 = bVar8, local_188 != (code *)0x0)) {
              local_5115 = bVar8;
              (*local_184)(auStack_190,&local_5115);
            }
            local_5117 = (byte)iVar11;
            if ((local_5117 != 0) ||
               (local_5117 = FUN_0801e104(puVar10,&local_5116), local_5117 != 0)) goto LAB_0802651e;
            if (local_5116 != '\0') {
              if (*DAT_080265d0 < 0x30) {
                FUN_080569f8(DAT_080265c4,DAT_080265c0,iVar16);
                if (*DAT_080265b4 == 3) {
                  iVar11 = 1;
                }
                else {
                  iVar11 = FUN_080216f8(DAT_080265c4,puVar10);
                  if (iVar11 == 0) {
                    if (((uint)local_180 != (uVar12 & 0xff)) &&
                       (local_180 = bVar8, local_188 != (code *)0x0)) {
                      local_5115 = bVar8;
                      (*local_184)(auStack_190,&local_5115);
                    }
                    *(uint *)(iVar9 + uVar14 * 4) = *(uint *)(iVar9 + uVar14 * 4) | uVar13;
                  }
                }
              }
              else {
                iVar11 = 9;
              }
              local_5117 = (byte)iVar11;
            }
            if (local_5117 != 0) goto LAB_0802651e;
            FUN_0804cb68(DAT_080265c8,iVar16);
          }
          uVar12 = uVar12 + 1;
          iVar16 = iVar16 + 1;
        } while (uVar12 != 0x30);
        FUN_0804cb68(DAT_080265cc,param_1 + 1);
      }
LAB_0802651e:
      if (local_5117 != 1) {
        FUN_0801d860(local_5117);
        goto LAB_08026234;
      }
    }
    else if (local_5117 != 1) {
      if (local_5117 != 0x12) {
        *DAT_080265b4 = 0;
        goto LAB_08026234;
      }
      goto LAB_0802642e;
    }
  }
  else if (local_5117 != 1) {
    if (local_5117 != 0x12) {
      *DAT_080263d4 = 0;
      goto LAB_08026234;
    }
LAB_0802642e:
    *DAT_080265b4 = 2;
    local_5117 = 0x12;
    goto LAB_08026234;
  }
  local_5117 = 1;
  *DAT_080265b4 = 3;
LAB_08026234:
  local_50 = uVar4;
  if (local_44 != (code *)0x0) {
    (*local_44)(auStack_4c,auStack_4c,3);
  }
  local_68 = uVar4;
  if (local_5c != (code *)0x0) {
    (*local_5c)(auStack_64,auStack_64,3);
  }
  local_8c = DAT_080263b0;
  if (local_80 != (code *)0x0) {
    (*local_80)(auStack_88,auStack_88,3);
  }
  if (local_9c != (code *)0x0) {
    (*local_9c)(auStack_a4,auStack_a4,3);
  }
  local_bc = DAT_080263c4;
  if (local_b0 != (code *)0x0) {
    (*local_b0)(auStack_b8,auStack_b8,3);
  }
  local_d4 = DAT_080263c0;
  if (local_c8 != (code *)0x0) {
    (*local_c8)(auStack_d0,auStack_d0,3);
  }
  local_ec = DAT_080263b4;
  if (local_e0 != (code *)0x0) {
    (*local_e0)(auStack_e8,auStack_e8,3);
  }
  local_104 = uVar2;
  if (local_f8 != (code *)0x0) {
    (*local_f8)(auStack_100,auStack_100,3);
  }
  local_11c = DAT_080263bc;
  if (local_110 != (code *)0x0) {
    (*local_110)(auStack_118,auStack_118,3);
  }
  local_134 = DAT_080263b8;
  if (local_128 != (code *)0x0) {
    (*local_128)(auStack_130,auStack_130,3);
  }
  if (local_144 != (code *)0x0) {
    (*local_144)(auStack_14c,auStack_14c,3);
  }
  local_164 = uVar2;
  if (local_158 != (code *)0x0) {
    (*local_158)(auStack_160,auStack_160,3);
  }
  local_17c = uVar2;
  if (local_170 != (code *)0x0) {
    (*local_170)(auStack_178,auStack_178,3);
  }
  local_194 = uVar2;
  if (local_188 != (code *)0x0) {
    (*local_188)(auStack_190,auStack_190,3);
  }
  puVar15 = &local_194;
  do {
    puVar15 = puVar15 + -0x27c;
    FUN_08010c78(puVar15);
  } while (puVar15 != puVar10);
  return local_5117;
}


```

---
## callers of `0x080277ac` (FUN_080277ac)

### `FUN_080142dc` @ `080142dc`
```c

void FUN_080142dc(void)

{
  int *piVar1;
  int **ppiVar2;
  int *piVar3;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  undefined *puVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  code *pcVar11;
  undefined4 *puVar12;
  int iVar13;
  undefined *puVar14;
  undefined4 *puVar15;
  undefined4 *puVar16;
  undefined *puVar17;
  int local_704;
  undefined local_700;
  undefined local_6ff;
  undefined local_6fe;
  undefined local_6fd;
  undefined local_6fc;
  undefined local_6fb;
  undefined local_6fa;
  undefined local_6f9;
  undefined local_6f8;
  undefined local_6f7;
  undefined local_6f6;
  undefined local_6f5;
  undefined local_6f4;
  undefined local_6f3;
  undefined local_6f2;
  undefined local_6f1;
  undefined local_6f0;
  undefined local_6ef;
  undefined local_6ee;
  undefined local_6ed;
  undefined local_6ec;
  undefined local_6eb;
  undefined local_6ea;
  undefined local_6e9;
  undefined local_6e8;
  undefined local_6e7;
  undefined local_6e6;
  undefined local_6e5;
  undefined local_6e4;
  undefined local_6e3;
  undefined2 local_6e2;
  undefined4 local_6e0;
  undefined4 local_6dc;
  undefined4 local_6d8;
  undefined4 local_6d4;
  undefined4 local_6d0;
  undefined4 local_6cc;
  undefined4 local_6c8;
  undefined4 local_6c4;
  int local_6c0;
  undefined4 local_6bc;
  undefined4 local_6b8;
  undefined4 local_6b4;
  undefined4 local_6b0;
  int local_6ac;
  undefined auStack_6a8 [8];
  code *local_6a0;
  undefined4 uStack_69c;
  undefined auStack_698 [8];
  code *local_690;
  undefined4 local_68c;
  undefined auStack_688 [8];
  code *local_680;
  undefined4 local_67c;
  undefined auStack_678 [8];
  code *local_670;
  undefined4 local_66c;
  undefined auStack_668 [8];
  code *local_660;
  undefined4 local_65c;
  undefined auStack_658 [8];
  code *local_650;
  undefined4 local_64c;
  undefined auStack_648 [8];
  code *local_640;
  undefined4 local_63c;
  undefined auStack_638 [8];
  code *local_630;
  undefined4 local_62c;
  undefined auStack_628 [8];
  code *local_620;
  undefined4 local_61c;
  undefined auStack_618 [8];
  code *local_610;
  undefined4 local_60c;
  undefined auStack_608 [8];
  code *local_600;
  undefined4 local_5fc;
  undefined auStack_5f8 [8];
  code *local_5f0;
  undefined4 local_5ec;
  undefined auStack_5e8 [8];
  code *local_5e0;
  undefined4 local_5dc;
  undefined auStack_5d8 [8];
  code *local_5d0;
  undefined4 local_5cc;
  undefined auStack_5c8 [8];
  code *local_5c0;
  undefined4 local_5bc;
  undefined auStack_5b8 [8];
  code *local_5b0;
  undefined4 local_5ac;
  undefined auStack_5a8 [8];
  code *local_5a0;
  undefined4 local_59c;
  undefined auStack_598 [8];
  code *local_590;
  undefined4 local_58c;
  undefined auStack_588 [8];
  code *local_580;
  undefined4 local_57c;
  undefined auStack_578 [8];
  code *local_570;
  undefined4 local_56c;
  undefined auStack_568 [8];
  code *local_560;
  undefined4 local_55c;
  undefined auStack_558 [8];
  code *local_550;
  undefined4 local_54c;
  undefined auStack_548 [8];
  code *local_540;
  undefined4 local_53c;
  undefined auStack_538 [8];
  code *local_530;
  undefined4 local_52c;
  undefined auStack_528 [8];
  code *local_520;
  undefined4 local_51c;
  undefined auStack_518 [8];
  code *local_510;
  undefined4 local_50c;
  undefined auStack_508 [8];
  code *local_500;
  undefined4 local_4fc;
  undefined auStack_4f8 [8];
  code *local_4f0;
  undefined4 local_4ec;
  undefined auStack_4e8 [8];
  code *local_4e0;
  undefined4 local_4dc;
  undefined auStack_4d8 [8];
  code *local_4d0;
  undefined4 local_4cc;
  undefined auStack_4c8 [8];
  code *local_4c0;
  undefined4 local_4bc;
  undefined auStack_4b8 [8];
  code *local_4b0;
  undefined4 local_4ac;
  undefined auStack_4a8 [8];
  code *local_4a0;
  undefined4 local_49c;
  undefined auStack_498 [8];
  code *local_490;
  undefined4 local_48c;
  undefined auStack_488 [8];
  code *local_480;
  undefined4 local_47c;
  undefined auStack_478 [8];
  code *local_470;
  undefined4 local_46c;
  undefined auStack_468 [8];
  code *local_460;
  undefined4 local_45c;
  undefined auStack_458 [8];
  code *local_450;
  undefined4 local_44c;
  undefined auStack_448 [8];
  code *local_440;
  undefined4 local_43c;
  undefined auStack_438 [8];
  code *local_430;
  undefined4 local_42c;
  undefined auStack_428 [8];
  code *local_420;
  undefined4 local_41c;
  undefined auStack_418 [8];
  code *local_410;
  undefined4 local_40c;
  undefined auStack_408 [8];
  code *local_400;
  undefined4 local_3fc;
  undefined auStack_3f8 [8];
  code *local_3f0;
  undefined4 local_3ec;
  undefined auStack_3e8 [8];
  code *local_3e0;
  undefined4 local_3dc;
  undefined auStack_3d8 [8];
  code *local_3d0;
  undefined4 local_3cc;
  undefined auStack_3c8 [8];
  code *local_3c0;
  undefined4 local_3bc;
  undefined auStack_3b8 [72];
  undefined auStack_370 [72];
  undefined auStack_328 [256];
  undefined4 local_228;
  undefined4 uStack_224;
  undefined4 local_128;
  undefined4 uStack_124;
  code *local_120;
  undefined4 local_11c;
  
  iVar7 = DAT_0801464c;
  FUN_0800b39c(DAT_080145f4);
  FUN_08009fc8();
  FUN_0803ebd0(3000);
  FUN_08027fd8();
  FUN_08009f8c();
  FUN_080088b8();
  FUN_0802b26c();
  FUN_0801facc();
  FUN_08009bcc(iVar7);
  FUN_08009ea4(DAT_080145f8);
  local_6a0 = DAT_08014600;
  uStack_69c = DAT_080145fc;
  FUN_0800c630(iVar7 + 4,auStack_6a8);
  local_700 = *(undefined *)(iVar7 + 0x14);
  if (*(int *)(iVar7 + 0xc) != 0) {
    (**(code **)(iVar7 + 0x10))(iVar7 + 4,&local_700);
    if (local_6a0 != (code *)0x0) {
      (*local_6a0)(auStack_6a8,auStack_6a8,3);
    }
    local_690 = DAT_08014608;
    puVar16 = DAT_08014604;
    local_11c = *(undefined4 *)(iVar7 + 0x28);
    local_120 = *(code **)(iVar7 + 0x24);
    *(code **)(iVar7 + 0x24) = DAT_08014608;
    local_68c = DAT_0801460c;
    *(undefined4 *)(iVar7 + 0x28) = DAT_0801460c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6e0 = *(undefined4 *)(iVar7 + 0x2c);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6e0 = *(undefined4 *)(iVar7 + 0x2c);
      if (*(int *)(iVar7 + 0x24) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x28))(DAT_08014604);
    if (local_690 != (code *)0x0) {
      (*local_690)(auStack_698,auStack_698,3);
    }
    puVar16 = DAT_08014614;
    local_680 = DAT_08014610;
    local_11c = *(undefined4 *)(iVar7 + 0x7c);
    local_120 = *(code **)(iVar7 + 0x78);
    *(code **)(iVar7 + 0x78) = DAT_08014610;
    local_67c = DAT_08014618;
    *(undefined4 *)(iVar7 + 0x7c) = DAT_08014618;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6ff = *(undefined *)(iVar7 + 0x81);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6ff = *(undefined *)(iVar7 + 0x81);
      if (*(int *)(iVar7 + 0x78) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x7c))(DAT_08014614);
    if (local_680 != (code *)0x0) {
      (*local_680)(auStack_688,auStack_688,3);
    }
    puVar16 = DAT_08014624;
    local_670 = DAT_08014620;
    local_66c = DAT_0801461c;
    local_120 = *(code **)(iVar7 + 0xa8);
    *(code **)(iVar7 + 0xa8) = DAT_08014620;
    local_11c = *(undefined4 *)(iVar7 + 0xac);
    *(undefined4 *)(iVar7 + 0xac) = local_66c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6fe = *(undefined *)(iVar7 + 0xb1);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6fe = *(undefined *)(iVar7 + 0xb1);
      if (*(int *)(iVar7 + 0xa8) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0xac))(DAT_08014624);
    if (local_670 != (code *)0x0) {
      (*local_670)(auStack_678,auStack_678,3);
    }
    puVar16 = DAT_08014630;
    local_660 = DAT_0801462c;
    local_65c = DAT_08014628;
    local_120 = *(code **)(iVar7 + 0x90);
    *(code **)(iVar7 + 0x90) = DAT_0801462c;
    local_11c = *(undefined4 *)(iVar7 + 0x94);
    *(undefined4 *)(iVar7 + 0x94) = local_65c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6fd = *(undefined *)(iVar7 + 0x99);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6fd = *(undefined *)(iVar7 + 0x99);
      if (*(int *)(iVar7 + 0x90) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x94))(DAT_08014630);
    if (local_660 != (code *)0x0) {
      (*local_660)(auStack_668,auStack_668,3);
    }
    puVar16 = DAT_0801463c;
    local_650 = DAT_08014638;
    local_64c = DAT_08014634;
    local_120 = *(code **)(iVar7 + 0x3c);
    *(code **)(iVar7 + 0x3c) = DAT_08014638;
    local_11c = *(undefined4 *)(iVar7 + 0x40);
    *(undefined4 *)(iVar7 + 0x40) = local_64c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6dc = *(undefined4 *)(iVar7 + 0x48);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6dc = *(undefined4 *)(iVar7 + 0x48);
      if (*(int *)(iVar7 + 0x3c) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x40))(DAT_0801463c);
    if (local_650 != (code *)0x0) {
      (*local_650)(auStack_658,auStack_658,3);
    }
    puVar16 = DAT_08014648;
    local_640 = DAT_08014644;
    local_63c = DAT_08014640;
    local_120 = *(code **)(iVar7 + 0xc0);
    *(code **)(iVar7 + 0xc0) = DAT_08014644;
    local_11c = *(undefined4 *)(iVar7 + 0xc4);
    *(undefined4 *)(iVar7 + 0xc4) = local_63c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6d8 = *(undefined4 *)(iVar7 + 0xcc);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6d8 = *(undefined4 *)(iVar7 + 0xcc);
      if (*(int *)(iVar7 + 0xc0) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0xc4))(DAT_08014648);
    if (local_640 != (code *)0x0) {
      (*local_640)(auStack_648,auStack_648,3);
    }
    puVar16 = DAT_0801496c;
    local_630 = DAT_08014968;
    local_62c = DAT_08014964;
    local_120 = *(code **)(iVar7 + 0xe4);
    *(code **)(iVar7 + 0xe4) = DAT_08014968;
    local_11c = *(undefined4 *)(iVar7 + 0xe8);
    *(undefined4 *)(iVar7 + 0xe8) = local_62c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6d4 = *(undefined4 *)(iVar7 + 0xf0);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6d4 = *(undefined4 *)(iVar7 + 0xf0);
      if (*(int *)(iVar7 + 0xe4) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0xe8))(DAT_0801496c);
    if (local_630 != (code *)0x0) {
      (*local_630)(auStack_638,auStack_638,3);
    }
    puVar16 = DAT_08014978;
    local_620 = DAT_08014974;
    local_61c = DAT_08014970;
    local_120 = *(code **)(iVar7 + 0x108);
    *(code **)(iVar7 + 0x108) = DAT_08014974;
    local_11c = *(undefined4 *)(iVar7 + 0x10c);
    *(undefined4 *)(iVar7 + 0x10c) = local_61c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6d0 = *(undefined4 *)(iVar7 + 0x114);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6d0 = *(undefined4 *)(iVar7 + 0x114);
      if (*(int *)(iVar7 + 0x108) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x10c))(DAT_08014978);
    if (local_620 != (code *)0x0) {
      (*local_620)(auStack_628,auStack_628,3);
    }
    puVar16 = DAT_08014984;
    local_610 = DAT_08014980;
    local_60c = DAT_0801497c;
    local_120 = *(code **)(iVar7 + 0x60);
    *(code **)(iVar7 + 0x60) = DAT_08014980;
    local_11c = *(undefined4 *)(iVar7 + 100);
    *(undefined4 *)(iVar7 + 100) = local_60c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6fc = *(undefined *)(iVar7 + 0x69);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6fc = *(undefined *)(iVar7 + 0x69);
      if (*(int *)(iVar7 + 0x60) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 100))(DAT_08014984);
    if (local_610 != (code *)0x0) {
      (*local_610)(auStack_618,auStack_618,3);
    }
    puVar16 = DAT_08014990;
    local_600 = DAT_0801498c;
    local_5fc = DAT_08014988;
    local_120 = *(code **)(iVar7 + 300);
    *(code **)(iVar7 + 300) = DAT_0801498c;
    local_11c = *(undefined4 *)(iVar7 + 0x130);
    *(undefined4 *)(iVar7 + 0x130) = local_5fc;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6fb = *(undefined *)(iVar7 + 0x135);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6fb = *(undefined *)(iVar7 + 0x135);
      if (*(int *)(iVar7 + 300) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x130))(DAT_08014990);
    if (local_600 != (code *)0x0) {
      (*local_600)(auStack_608,auStack_608,3);
    }
    puVar16 = DAT_0801499c;
    local_5f0 = DAT_08014998;
    local_5ec = DAT_08014994;
    local_120 = *(code **)(iVar7 + 0x144);
    *(code **)(iVar7 + 0x144) = DAT_08014998;
    local_11c = *(undefined4 *)(iVar7 + 0x148);
    *(undefined4 *)(iVar7 + 0x148) = local_5ec;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6fa = *(undefined *)(iVar7 + 0x14d);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6fa = *(undefined *)(iVar7 + 0x14d);
      if (*(int *)(iVar7 + 0x144) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x148))(DAT_0801499c);
    if (local_5f0 != (code *)0x0) {
      (*local_5f0)(auStack_5f8,auStack_5f8,3);
    }
    puVar16 = DAT_080149a8;
    local_5e0 = DAT_080149a4;
    local_5dc = DAT_080149a0;
    local_120 = *(code **)(iVar7 + 0x15c);
    *(code **)(iVar7 + 0x15c) = DAT_080149a4;
    local_11c = *(undefined4 *)(iVar7 + 0x160);
    *(undefined4 *)(iVar7 + 0x160) = local_5dc;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6f9 = *(undefined *)(iVar7 + 0x165);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6f9 = *(undefined *)(iVar7 + 0x165);
      if (*(int *)(iVar7 + 0x15c) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x160))(DAT_080149a8);
    if (local_5e0 != (code *)0x0) {
      (*local_5e0)(auStack_5e8,auStack_5e8,3);
    }
    puVar16 = DAT_080149b4;
    local_5d0 = DAT_080149b0;
    local_5cc = DAT_080149ac;
    local_120 = *(code **)(iVar7 + 0x174);
    *(code **)(iVar7 + 0x174) = DAT_080149b0;
    local_11c = *(undefined4 *)(iVar7 + 0x178);
    *(undefined4 *)(iVar7 + 0x178) = local_5cc;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6f8 = *(undefined *)(iVar7 + 0x17d);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6f8 = *(undefined *)(iVar7 + 0x17d);
      if (*(int *)(iVar7 + 0x174) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x178))(DAT_080149b4);
    if (local_5d0 != (code *)0x0) {
      (*local_5d0)(auStack_5d8,auStack_5d8,3);
    }
    puVar16 = DAT_08014cb8;
    local_5c0 = DAT_08014cb4;
    local_5bc = DAT_08014cb0;
    local_120 = *(code **)(iVar7 + 0x18c);
    *(code **)(iVar7 + 0x18c) = DAT_08014cb4;
    local_11c = *(undefined4 *)(iVar7 + 400);
    *(undefined4 *)(iVar7 + 400) = local_5bc;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6cc = *(undefined4 *)(iVar7 + 0x198);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6cc = *(undefined4 *)(iVar7 + 0x198);
      if (*(int *)(iVar7 + 0x18c) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 400))(DAT_08014cb8);
    if (local_5c0 != (code *)0x0) {
      (*local_5c0)(auStack_5c8,auStack_5c8,3);
    }
    puVar16 = DAT_08014cc4;
    local_5b0 = DAT_08014cc0;
    local_5ac = DAT_08014cbc;
    local_120 = *(code **)(iVar7 + 0x1b0);
    *(code **)(iVar7 + 0x1b0) = DAT_08014cc0;
    local_11c = *(undefined4 *)(iVar7 + 0x1b4);
    *(undefined4 *)(iVar7 + 0x1b4) = local_5ac;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6f7 = *(undefined *)(iVar7 + 0x1b9);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6f7 = *(undefined *)(iVar7 + 0x1b9);
      if (*(int *)(iVar7 + 0x1b0) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x1b4))(DAT_08014cc4);
    if (local_5b0 != (code *)0x0) {
      (*local_5b0)(auStack_5b8,auStack_5b8,3);
    }
    puVar16 = DAT_08014cd0;
    local_5a0 = DAT_08014ccc;
    local_59c = DAT_08014cc8;
    local_120 = *(code **)(iVar7 + 0x1c8);
    *(code **)(iVar7 + 0x1c8) = DAT_08014ccc;
    local_11c = *(undefined4 *)(iVar7 + 0x1cc);
    *(undefined4 *)(iVar7 + 0x1cc) = local_59c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar4 = *puVar16;
    uVar9 = puVar16[1];
    *puVar16 = local_128;
    puVar16[1] = uStack_124;
    local_128 = uVar4;
    uStack_124 = uVar9;
    if (local_120 == (code *)0x0) {
      local_6f6 = *(undefined *)(iVar7 + 0x1d1);
    }
    else {
      (*local_120)(&local_128,&local_128,3);
      local_6f6 = *(undefined *)(iVar7 + 0x1d1);
      if (*(int *)(iVar7 + 0x1c8) == 0) goto LAB_0801515a;
    }
    (**(code **)(iVar7 + 0x1cc))(DAT_08014cd0);
    if (local_5a0 != (code *)0x0) {
      (*local_5a0)(auStack_5a8,auStack_5a8,3);
    }
    iVar13 = DAT_08014cd4;
    local_58c = DAT_08014cd8;
    local_590 = DAT_08014cdc;
    FUN_0800c630(DAT_08014cd4 + 0x5b8,auStack_598);
    local_6f5 = *(undefined *)(iVar13 + 0x5c9);
    if (*(int *)(iVar13 + 0x5c0) != 0) {
      (**(code **)(iVar13 + 0x5c4))(iVar13 + 0x5b8,&local_6f5);
      if (local_590 != (code *)0x0) {
        (*local_590)(auStack_598,auStack_598,3);
      }
      local_580 = DAT_08014ce0;
      local_11c = *(undefined4 *)(iVar13 + 0x5dc);
      local_120 = *(code **)(iVar13 + 0x5d8);
      *(code **)(iVar13 + 0x5d8) = DAT_08014ce0;
      local_57c = DAT_08014ce4;
      *(undefined4 *)(iVar13 + 0x5dc) = DAT_08014ce4;
      local_228 = local_128;
      uStack_224 = uStack_124;
      uVar4 = *(undefined4 *)(iVar13 + 0x5d0);
      uVar9 = *(undefined4 *)(iVar13 + 0x5d4);
      *(undefined4 *)(iVar13 + 0x5d0) = local_128;
      *(undefined4 *)(iVar13 + 0x5d4) = uStack_124;
      local_128 = uVar4;
      uStack_124 = uVar9;
      if (local_120 == (code *)0x0) {
        local_6f4 = *(undefined *)(iVar13 + 0x5e1);
      }
      else {
        (*local_120)(&local_128,&local_128,3);
        local_6f4 = *(undefined *)(iVar13 + 0x5e1);
        if (*(int *)(iVar13 + 0x5d8) == 0) goto LAB_0801515a;
      }
      (**(code **)(iVar13 + 0x5dc))(DAT_08014ce8);
      if (local_580 != (code *)0x0) {
        (*local_580)(auStack_588,auStack_588,3);
      }
      local_570 = DAT_08014cf0;
      local_56c = DAT_08014cec;
      local_120 = *(code **)(iVar13 + 0x638);
      local_11c = *(undefined4 *)(iVar13 + 0x63c);
      *(code **)(iVar13 + 0x638) = DAT_08014cf0;
      *(undefined4 *)(iVar13 + 0x63c) = local_56c;
      local_228 = local_128;
      uStack_224 = uStack_124;
      uVar4 = *(undefined4 *)(iVar13 + 0x630);
      uVar9 = *(undefined4 *)(iVar13 + 0x634);
      *(undefined4 *)(iVar13 + 0x630) = local_128;
      *(undefined4 *)(iVar13 + 0x634) = uStack_124;
      local_128 = uVar4;
      uStack_124 = uVar9;
      if (local_120 == (code *)0x0) {
        local_6c8 = *(undefined4 *)(iVar13 + 0x644);
      }
      else {
        (*local_120)(&local_128,&local_128,3);
        local_6c8 = *(undefined4 *)(iVar13 + 0x644);
        if (*(int *)(iVar13 + 0x638) == 0) goto LAB_0801515a;
      }
      (**(code **)(iVar13 + 0x63c))(DAT_08014cf4);
      if (local_570 != (code *)0x0) {
        (*local_570)(auStack_578,auStack_578,3);
      }
      iVar13 = DAT_08014cf8;
      local_55c = DAT_08014cfc;
      local_560 = DAT_08014d00;
      FUN_0800c630(DAT_08014cf8 + 0xf84,auStack_568);
      local_6f3 = *(undefined *)(iVar13 + 0xf94);
      if (*(int *)(iVar13 + 0xf8c) != 0) {
        (**(code **)(iVar13 + 0xf90))(iVar13 + 0xf84,&local_6f3);
        if (local_560 != (code *)0x0) {
          (*local_560)(auStack_568,auStack_568,3);
        }
        local_54c = DAT_08014d04;
        local_550 = DAT_08014d08;
        FUN_0800c630(DAT_08014d0c,auStack_558);
        local_6f2 = *(undefined *)(iVar13 + 0xfc4);
        if (*(int *)(iVar13 + 0xfbc) != 0) {
          (**(code **)(iVar13 + 0xfc0))(DAT_08014d0c,&local_6f2);
          if (local_550 != (code *)0x0) {
            (*local_550)(auStack_558,auStack_558,3);
          }
          local_540 = DAT_08014d14;
          local_53c = DAT_08014d10;
          local_120 = *(code **)(iVar13 + 0xfa4);
          local_11c = *(undefined4 *)(iVar13 + 0xfa8);
          *(code **)(iVar13 + 0xfa4) = DAT_08014d14;
          *(undefined4 *)(iVar13 + 0xfa8) = local_53c;
          local_228 = local_128;
          uStack_224 = uStack_124;
          uVar4 = *(undefined4 *)(iVar13 + 0xf9c);
          uVar9 = *(undefined4 *)(iVar13 + 4000);
          *(undefined4 *)(iVar13 + 0xf9c) = local_128;
          *(undefined4 *)(iVar13 + 4000) = uStack_124;
          local_128 = uVar4;
          uStack_124 = uVar9;
          if (local_120 == (code *)0x0) {
            local_6f1 = *(undefined *)(iVar13 + 0xfac);
          }
          else {
            (*local_120)(&local_128,&local_128,3);
            local_6f1 = *(undefined *)(iVar13 + 0xfac);
            if (*(int *)(iVar13 + 0xfa4) == 0) goto LAB_0801515a;
          }
          (**(code **)(iVar13 + 0xfa8))(DAT_08015054);
          if (local_540 != (code *)0x0) {
            (*local_540)(auStack_548,auStack_548,3);
          }
          local_530 = DAT_0801505c;
          local_52c = DAT_08015058;
          local_120 = *(code **)(iVar13 + 0xfd0);
          local_11c = *(undefined4 *)(iVar13 + 0xfd4);
          *(code **)(iVar13 + 0xfd0) = DAT_0801505c;
          *(undefined4 *)(iVar13 + 0xfd4) = local_52c;
          local_228 = local_128;
          uStack_224 = uStack_124;
          uVar4 = *(undefined4 *)(iVar13 + 0xfc8);
          uVar9 = *(undefined4 *)(iVar13 + 0xfcc);
          *(undefined4 *)(iVar13 + 0xfc8) = local_128;
          *(undefined4 *)(iVar13 + 0xfcc) = uStack_124;
          local_128 = uVar4;
          uStack_124 = uVar9;
          if (local_120 == (code *)0x0) {
            local_6f0 = *(undefined *)(iVar13 + 0xfd8);
          }
          else {
            (*local_120)(&local_128,&local_128,3);
            local_6f0 = *(undefined *)(iVar13 + 0xfd8);
            local_6c4 = 0;
            if (*(int *)(iVar13 + 0xfd0) == 0) goto LAB_0801515a;
          }
          local_6c4 = 0;
          (**(code **)(iVar13 + 0xfd4))(DAT_08015060,&local_6c4,&local_6f0);
          local_6f0 = *(undefined *)(iVar13 + 0xfd9);
          local_6c4 = 1;
          if (*(int *)(iVar13 + 0xfd0) != 0) {
            (**(code **)(iVar13 + 0xfd4))(DAT_08015060,&local_6c4,&local_6f0);
            if (local_530 != (code *)0x0) {
              (*local_530)(auStack_538,auStack_538,3);
            }
            local_520 = DAT_08015068;
            local_51c = DAT_08015064;
            local_120 = *(code **)(iVar13 + 0xfec);
            local_11c = *(undefined4 *)(iVar13 + 0xff0);
            *(code **)(iVar13 + 0xfec) = DAT_08015068;
            *(undefined4 *)(iVar13 + 0xff0) = local_51c;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar13 + 0xfe4);
            uVar9 = *(undefined4 *)(iVar13 + 0xfe8);
            *(undefined4 *)(iVar13 + 0xfe4) = local_128;
            *(undefined4 *)(iVar13 + 0xfe8) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6ef = *(undefined *)(iVar13 + 0xff5);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6ef = *(undefined *)(iVar13 + 0xff5);
              if (*(int *)(iVar13 + 0xfec) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar13 + 0xff0))(DAT_0801506c);
            if (local_520 != (code *)0x0) {
              (*local_520)(auStack_528,auStack_528,3);
            }
            local_510 = DAT_08015078;
            iVar5 = DAT_08015074;
            local_50c = DAT_08015070;
            local_120 = *(code **)(DAT_08015074 + 4);
            local_11c = *(undefined4 *)(DAT_08015074 + 8);
            *(code **)(DAT_08015074 + 4) = DAT_08015078;
            *(undefined4 *)(iVar5 + 8) = local_50c;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar13 + 0xffc);
            uVar9 = *(undefined4 *)(iVar13 + 0x1000);
            *(undefined4 *)(iVar13 + 0xffc) = local_128;
            *(undefined4 *)(iVar13 + 0x1000) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6ee = *(undefined *)(iVar5 + 0xd);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6ee = *(undefined *)(iVar5 + 0xd);
              if (*(int *)(iVar5 + 4) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar5 + 8))(DAT_0801507c);
            if (local_510 != (code *)0x0) {
              (*local_510)(auStack_518,auStack_518,3);
            }
            local_500 = DAT_08015084;
            local_4fc = DAT_08015080;
            local_120 = *(code **)(iVar5 + 0x1c);
            local_11c = *(undefined4 *)(iVar5 + 0x20);
            *(code **)(iVar5 + 0x1c) = DAT_08015084;
            *(undefined4 *)(iVar5 + 0x20) = local_4fc;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar5 + 0x14);
            uVar9 = *(undefined4 *)(iVar5 + 0x18);
            *(undefined4 *)(iVar5 + 0x14) = local_128;
            *(undefined4 *)(iVar5 + 0x18) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6ed = *(undefined *)(iVar5 + 0x24);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6ed = *(undefined *)(iVar5 + 0x24);
              if (*(int *)(iVar5 + 0x1c) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar5 + 0x20))(DAT_08015088);
            if (local_500 != (code *)0x0) {
              (*local_500)(auStack_508,auStack_508,3);
            }
            local_4f0 = DAT_08015090;
            local_4ec = DAT_0801508c;
            local_120 = *(code **)(iVar5 + 0x34);
            local_11c = *(undefined4 *)(iVar5 + 0x38);
            *(code **)(iVar5 + 0x34) = DAT_08015090;
            *(undefined4 *)(iVar5 + 0x38) = local_4ec;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar5 + 0x2c);
            uVar9 = *(undefined4 *)(iVar5 + 0x30);
            *(undefined4 *)(iVar5 + 0x2c) = local_128;
            *(undefined4 *)(iVar5 + 0x30) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6ec = *(undefined *)(iVar5 + 0x3d);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6ec = *(undefined *)(iVar5 + 0x3d);
              if (*(int *)(iVar5 + 0x34) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar5 + 0x38))(DAT_08015094);
            if (local_4f0 != (code *)0x0) {
              (*local_4f0)(auStack_4f8,auStack_4f8,3);
            }
            local_4e0 = DAT_0801509c;
            local_4dc = DAT_08015098;
            local_120 = *(code **)(iVar5 + 0x4c);
            local_11c = *(undefined4 *)(iVar5 + 0x50);
            *(code **)(iVar5 + 0x4c) = DAT_0801509c;
            *(undefined4 *)(iVar5 + 0x50) = local_4dc;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar5 + 0x44);
            uVar9 = *(undefined4 *)(iVar5 + 0x48);
            *(undefined4 *)(iVar5 + 0x44) = local_128;
            *(undefined4 *)(iVar5 + 0x48) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6eb = *(undefined *)(iVar5 + 0x55);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6eb = *(undefined *)(iVar5 + 0x55);
              if (*(int *)(iVar5 + 0x4c) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar5 + 0x50))(DAT_080150a0);
            if (local_4e0 != (code *)0x0) {
              (*local_4e0)(auStack_4e8,auStack_4e8,3);
            }
            local_4d0 = DAT_080150a8;
            local_4cc = DAT_080150a4;
            local_120 = *(code **)(iVar5 + 100);
            local_11c = *(undefined4 *)(iVar5 + 0x68);
            *(code **)(iVar5 + 100) = DAT_080150a8;
            *(undefined4 *)(iVar5 + 0x68) = local_4cc;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar5 + 0x5c);
            uVar9 = *(undefined4 *)(iVar5 + 0x60);
            *(undefined4 *)(iVar5 + 0x5c) = local_128;
            *(undefined4 *)(iVar5 + 0x60) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 == (code *)0x0) {
              local_6ea = *(undefined *)(iVar5 + 0x6d);
            }
            else {
              (*local_120)(&local_128,&local_128,3);
              local_6ea = *(undefined *)(iVar5 + 0x6d);
              if (*(int *)(iVar5 + 100) == 0) goto LAB_0801515a;
            }
            (**(code **)(iVar5 + 0x68))(DAT_08015160);
            if (local_4d0 != (code *)0x0) {
              (*local_4d0)(auStack_4d8,auStack_4d8,3);
            }
            pcVar11 = DAT_08015168;
            local_11c = *(undefined4 *)(iVar5 + 0x7c);
            local_4bc = DAT_08015164;
            *(undefined4 *)(iVar5 + 0x7c) = DAT_08015164;
            local_120 = *(code **)(iVar5 + 0x78);
            *(code **)(iVar5 + 0x78) = pcVar11;
            local_4c0 = pcVar11;
            local_228 = local_128;
            uStack_224 = uStack_124;
            uVar4 = *(undefined4 *)(iVar5 + 0x70);
            uVar9 = *(undefined4 *)(iVar5 + 0x74);
            *(undefined4 *)(iVar5 + 0x70) = local_128;
            *(undefined4 *)(iVar5 + 0x74) = uStack_124;
            local_128 = uVar4;
            uStack_124 = uVar9;
            if (local_120 != (code *)0x0) {
              (*local_120)(&local_128,&local_128,3);
              pcVar11 = *(code **)(iVar5 + 0x78);
            }
            puVar17 = DAT_0801516c + -0x10;
            local_6e9 = *DAT_0801516c;
            local_6c0 = 0;
            puVar14 = DAT_0801516c;
            while (pcVar11 != (code *)0x0) {
              puVar14 = puVar14 + 1;
              iVar13 = local_6c0 + 1;
              (**(code **)(iVar5 + 0x7c))(puVar17,&local_6c0,&local_6e9);
              if (iVar13 == 4) {
                if (local_4c0 != (code *)0x0) {
                  (*local_4c0)(auStack_4c8,auStack_4c8,3);
                }
                local_4b0 = DAT_08015478;
                local_4ac = DAT_08015474;
                local_120 = *(code **)(iVar5 + 0x94);
                local_11c = *(undefined4 *)(iVar5 + 0x98);
                *(code **)(iVar5 + 0x94) = DAT_08015478;
                *(undefined4 *)(iVar5 + 0x98) = local_4ac;
                local_228 = local_128;
                uStack_224 = uStack_124;
                uVar4 = *(undefined4 *)(iVar5 + 0x8c);
                uVar9 = *(undefined4 *)(iVar5 + 0x90);
                *(undefined4 *)(iVar5 + 0x8c) = local_128;
                *(undefined4 *)(iVar5 + 0x90) = uStack_124;
                local_128 = uVar4;
                uStack_124 = uVar9;
                if (local_120 == (code *)0x0) {
                  local_6bc = *(undefined4 *)(iVar5 + 0xa0);
                }
                else {
                  (*local_120)(&local_128,&local_128,3);
                  local_6bc = *(undefined4 *)(iVar5 + 0xa0);
                  if (*(int *)(iVar5 + 0x94) == 0) break;
                }
                (**(code **)(iVar5 + 0x98))(DAT_0801547c);
                if (local_4b0 != (code *)0x0) {
                  (*local_4b0)(auStack_4b8,auStack_4b8,3);
                }
                local_704 = 0;
                puVar16 = DAT_08015480;
                goto LAB_080151f0;
              }
              local_6e9 = *puVar14;
              local_6c0 = iVar13;
              pcVar11 = *(code **)(iVar5 + 0x78);
            }
          }
        }
      }
    }
  }
LAB_0801515a:
                    /* WARNING: Subroutine does not return */
  FUN_08054154();
LAB_080151f0:
  do {
    puVar12 = puVar16 + -0x16;
    FUN_08012e34(local_704);
    uVar4 = DAT_08015488;
    pcVar11 = DAT_08015484;
    local_4a0 = DAT_08015484;
    local_49c = DAT_08015488;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[-0x15];
    *puVar12 = local_128;
    puVar16[-0x15] = uStack_124;
    local_120 = (code *)puVar16[-0x14];
    local_11c = puVar16[-0x13];
    puVar16[-0x14] = pcVar11;
    puVar16[-0x13] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[-0x14];
    }
    local_6e8 = *(undefined *)((int)puVar16 + -0x47);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[-0x13])(puVar12,&local_6e8);
    if (local_4a0 != (code *)0x0) {
      (*local_4a0)(auStack_4a8,auStack_4a8,3);
    }
    uVar4 = DAT_08015490;
    pcVar11 = DAT_0801548c;
    puVar12 = puVar16 + -10;
    local_490 = DAT_0801548c;
    local_48c = DAT_08015490;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[-9];
    *puVar12 = local_128;
    puVar16[-9] = uStack_124;
    local_120 = (code *)puVar16[-8];
    local_11c = puVar16[-7];
    puVar16[-8] = pcVar11;
    puVar16[-7] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[-8];
    }
    local_6e7 = *(undefined *)((int)puVar16 + -0x17);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[-7])(puVar12,&local_6e7);
    if (local_490 != (code *)0x0) {
      (*local_490)(auStack_498,auStack_498,3);
    }
    uVar4 = DAT_08015498;
    pcVar11 = DAT_08015494;
    puVar12 = puVar16 + -0x10;
    local_480 = DAT_08015494;
    local_47c = DAT_08015498;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[-0xf];
    *puVar12 = local_128;
    puVar16[-0xf] = uStack_124;
    local_120 = (code *)puVar16[-0xe];
    local_11c = puVar16[-0xd];
    puVar16[-0xe] = pcVar11;
    puVar16[-0xd] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[-0xe];
    }
    local_6e6 = *(undefined *)((int)puVar16 + -0x2f);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[-0xd])(puVar12,&local_6e6);
    if (local_480 != (code *)0x0) {
      (*local_480)(auStack_488,auStack_488,3);
    }
    uVar4 = DAT_080154a0;
    pcVar11 = DAT_0801549c;
    puVar12 = puVar16 + -4;
    local_470 = DAT_0801549c;
    local_46c = DAT_080154a0;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[-3];
    *puVar12 = local_128;
    puVar16[-3] = uStack_124;
    local_120 = (code *)puVar16[-2];
    local_11c = puVar16[-1];
    puVar16[-2] = pcVar11;
    puVar16[-1] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[-2];
    }
    local_6e2 = *(undefined2 *)puVar16;
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[-1])(puVar12,&local_6e2);
    if (local_470 != (code *)0x0) {
      (*local_470)(auStack_478,auStack_478,3);
    }
    uVar4 = DAT_080154a8;
    pcVar11 = DAT_080154a4;
    puVar12 = puVar16 + 0xe3;
    local_460 = DAT_080154a4;
    local_45c = DAT_080154a8;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0xe4];
    *puVar12 = local_128;
    puVar16[0xe4] = uStack_124;
    local_120 = (code *)puVar16[0xe5];
    local_11c = puVar16[0xe6];
    puVar16[0xe5] = pcVar11;
    puVar16[0xe6] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[0xe5];
    }
    local_6e5 = *(undefined *)((int)puVar16 + 0x39d);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[0xe6])(puVar12,&local_6e5);
    if (local_460 != (code *)0x0) {
      (*local_460)(auStack_468,auStack_468,3);
    }
    uVar4 = DAT_080154b0;
    pcVar11 = DAT_080154ac;
    puVar12 = puVar16 + 0xe9;
    local_450 = DAT_080154ac;
    local_44c = DAT_080154b0;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0xea];
    *puVar12 = local_128;
    puVar16[0xea] = uStack_124;
    local_120 = (code *)puVar16[0xeb];
    local_11c = puVar16[0xec];
    puVar16[0xeb] = pcVar11;
    puVar16[0xec] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[0xeb];
    }
    local_6b8 = puVar16[0xee];
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[0xec])(puVar12,&local_6b8);
    if (local_450 != (code *)0x0) {
      (*local_450)(auStack_458,auStack_458,3);
    }
    uVar4 = DAT_0801578c;
    pcVar11 = DAT_08015788;
    puVar12 = puVar16 + 0xf2;
    local_440 = DAT_08015788;
    local_43c = DAT_0801578c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0xf3];
    *puVar12 = local_128;
    puVar16[0xf3] = uStack_124;
    local_120 = (code *)puVar16[0xf4];
    local_11c = puVar16[0xf5];
    puVar16[0xf4] = pcVar11;
    puVar16[0xf5] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[0xf4];
    }
    local_6e4 = *(undefined *)((int)puVar16 + 0x3d9);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[0xf5])(puVar12,&local_6e4);
    if (local_440 != (code *)0x0) {
      (*local_440)(auStack_448,auStack_448,3);
    }
    uVar4 = DAT_08015794;
    pcVar11 = DAT_08015790;
    puVar12 = puVar16 + 2;
    local_430 = DAT_08015790;
    local_42c = DAT_08015794;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[3];
    *puVar12 = local_128;
    puVar16[3] = uStack_124;
    local_120 = (code *)puVar16[4];
    local_11c = puVar16[5];
    puVar16[4] = pcVar11;
    puVar16[5] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[4];
    }
    local_6b4 = puVar16[6];
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[5])(puVar12,&local_6b4);
    if (local_430 != (code *)0x0) {
      (*local_430)(auStack_438,auStack_438,3);
    }
    uVar4 = DAT_0801579c;
    pcVar11 = DAT_08015798;
    puVar12 = puVar16 + 8;
    local_420 = DAT_08015798;
    local_41c = DAT_0801579c;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[9];
    *puVar12 = local_128;
    puVar16[9] = uStack_124;
    local_120 = (code *)puVar16[10];
    local_11c = puVar16[0xb];
    puVar16[10] = pcVar11;
    puVar16[0xb] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[10];
    }
    local_6b0 = puVar16[0xc];
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[0xb])(puVar12,&local_6b0);
    if (local_420 != (code *)0x0) {
      (*local_420)(auStack_428,auStack_428,3);
    }
    uVar4 = DAT_080157a4;
    pcVar11 = DAT_080157a0;
    puVar12 = puVar16 + 0xe;
    local_410 = DAT_080157a0;
    local_40c = DAT_080157a4;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0xf];
    *puVar12 = local_128;
    puVar16[0xf] = uStack_124;
    local_120 = (code *)puVar16[0x10];
    local_11c = puVar16[0x11];
    puVar16[0x10] = pcVar11;
    puVar16[0x11] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
      pcVar11 = (code *)puVar16[0x10];
    }
    local_6e3 = *(undefined *)(puVar16 + 0x12);
    if (pcVar11 == (code *)0x0) goto LAB_0801515a;
    (*(code *)puVar16[0x11])(puVar12,&local_6e3);
    if (local_410 != (code *)0x0) {
      (*local_410)(auStack_418,auStack_418,3);
    }
    pcVar11 = DAT_080157ac;
    uVar4 = DAT_080157a8;
    puVar12 = puVar16 + 0x14;
    local_3fc = DAT_080157a8;
    local_400 = DAT_080157ac;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0x15];
    *puVar12 = local_128;
    puVar16[0x15] = uStack_124;
    local_120 = (code *)puVar16[0x16];
    local_11c = puVar16[0x17];
    puVar16[0x16] = pcVar11;
    puVar16[0x17] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
    }
    FUN_08007160(auStack_328,puVar16 + 0x18,0x100);
    if (puVar16[0x16] == 0) goto LAB_0801515a;
    (*(code *)puVar16[0x17])(puVar12,auStack_328);
    if (local_400 != (code *)0x0) {
      (*local_400)(auStack_408,auStack_408,3);
    }
    pcVar11 = DAT_080157b4;
    uVar4 = DAT_080157b0;
    puVar12 = puVar16 + 0x59;
    local_3ec = DAT_080157b0;
    local_3f0 = DAT_080157b4;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0x5a];
    *puVar12 = local_128;
    puVar16[0x5a] = uStack_124;
    local_120 = (code *)puVar16[0x5b];
    local_11c = puVar16[0x5c];
    puVar16[0x5b] = pcVar11;
    puVar16[0x5c] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
    }
    FUN_08007160(&local_228,puVar16 + 0x5d,0x100);
    if (puVar16[0x5b] == 0) goto LAB_0801515a;
    (*(code *)puVar16[0x5c])(puVar12,&local_228);
    if (local_3f0 != (code *)0x0) {
      (*local_3f0)(auStack_3f8,auStack_3f8,3);
    }
    pcVar11 = DAT_080157bc;
    uVar4 = DAT_080157b8;
    puVar12 = puVar16 + 0x9e;
    local_3dc = DAT_080157b8;
    local_3e0 = DAT_080157bc;
    local_228 = local_128;
    uStack_224 = uStack_124;
    uVar9 = *puVar12;
    uVar10 = puVar16[0x9f];
    *puVar12 = local_128;
    puVar16[0x9f] = uStack_124;
    local_120 = (code *)puVar16[0xa0];
    local_11c = puVar16[0xa1];
    puVar16[0xa0] = pcVar11;
    puVar16[0xa1] = uVar4;
    local_128 = uVar9;
    uStack_124 = uVar10;
    if (local_120 != (code *)0x0) {
      (*local_120)(&local_128,&local_128,3);
    }
    FUN_08007160(&local_128,puVar16 + 0xa2,0x100);
    if (puVar16[0xa0] == 0) goto LAB_0801515a;
    (*(code *)puVar16[0xa1])(puVar12,&local_128);
    if (local_3e0 != (code *)0x0) {
      (*local_3e0)(auStack_3e8,auStack_3e8,3);
    }
    puVar12 = puVar16 + -0x132;
    do {
      while( true ) {
        pcVar11 = DAT_08015ae0;
        uVar4 = DAT_08015adc;
        puVar15 = puVar12 + -0x16;
        local_3cc = DAT_08015adc;
        local_3d0 = DAT_08015ae0;
        local_228 = local_128;
        uStack_224 = uStack_124;
        uVar9 = *puVar15;
        uVar10 = puVar12[-0x15];
        *puVar15 = local_128;
        puVar12[-0x15] = uStack_124;
        local_120 = (code *)puVar12[-0x14];
        local_11c = puVar12[-0x13];
        puVar12[-0x14] = pcVar11;
        puVar12[-0x13] = uVar4;
        local_128 = uVar9;
        uStack_124 = uVar10;
        if (local_120 != (code *)0x0) {
          (*local_120)(&local_128,&local_128,3);
        }
        FUN_08007160(auStack_3b8,puVar12 + -0x12,0x48);
        if (puVar12[-0x14] == 0) goto LAB_0801515a;
        (*(code *)puVar12[-0x13])(puVar15,auStack_3b8);
        if (local_3d0 != (code *)0x0) {
          (*local_3d0)(auStack_3d8,auStack_3d8,3);
        }
        uVar4 = DAT_08015ae4;
        local_11c = puVar12[3];
        local_120 = (code *)puVar12[2];
        local_3bc = DAT_08015ae4;
        local_3c0 = DAT_08015ae8;
        puVar12[2] = DAT_08015ae8;
        puVar12[3] = uVar4;
        local_228 = local_128;
        uStack_224 = uStack_124;
        uVar4 = *puVar12;
        uVar9 = puVar12[1];
        *puVar12 = local_128;
        puVar12[1] = uStack_124;
        pcVar11 = DAT_08015ae8;
        local_128 = uVar4;
        uStack_124 = uVar9;
        if (local_120 != (code *)0x0) {
          (*local_120)(&local_128,&local_128,3);
          pcVar11 = (code *)puVar12[2];
        }
        iVar13 = 0;
        puVar15 = puVar12;
        while( true ) {
          local_6ac = iVar13;
          FUN_08007160(auStack_370,puVar15 + 4,0x48);
          if (pcVar11 == (code *)0x0) goto LAB_0801515a;
          iVar13 = iVar13 + 1;
          puVar15 = puVar15 + 0x12;
          (*(code *)puVar12[3])(puVar12,&local_6ac,auStack_370);
          if (iVar13 == 4) break;
          pcVar11 = (code *)puVar12[2];
        }
        puVar12 = puVar12 + 0x99;
        if (local_3c0 == (code *)0x0) break;
        (*local_3c0)(auStack_3c8,auStack_3c8,3);
        if (puVar12 == puVar16) goto LAB_080158ec;
      }
    } while (puVar12 != puVar16);
LAB_080158ec:
    puVar16 = puVar16 + 0x27c;
    local_704 = local_704 + 1;
  } while (local_704 != 8);
  local_128 = DAT_08015aec;
  local_11c = DAT_08015af0;
  local_120 = DAT_08015af4;
  FUN_08008a00(&local_128);
  if (local_120 != (code *)0x0) {
    (*local_120)(&local_128,&local_128,3);
  }
  FUN_080081ec();
  FUN_0802867c();
  iVar13 = FUN_08028770();
  if (iVar13 == 0) {
    software_bkpt(0);
    FUN_08008214();
    iVar13 = FUN_0802c818(6);
    puVar16 = DAT_08015e7c;
  }
  else {
    FUN_08008214();
    iVar13 = FUN_0802c818(6);
    puVar16 = DAT_08015e7c;
  }
  DAT_08015e7c = puVar16;
  if (iVar13 == 0) {
    iVar5 = FUN_0802c818(9);
    iVar13 = 0;
  }
  else {
    iVar13 = 0;
    FUN_08009fbc();
    FUN_0800a6e4();
    FUN_0800a60c(*DAT_08015e88);
    FUN_0800a014();
    FUN_0803ebd0(0x7d);
    FUN_080280d8();
    do {
      while (-1 < iVar13 << 0x1f) {
        iVar13 = iVar13 + 1;
        FUN_0800a60c(*puVar16);
        FUN_0800a014();
        FUN_0803ebd0(0x7d);
        if (iVar13 == 8) goto LAB_08015c9c;
      }
      iVar13 = iVar13 + 1;
      FUN_0800a6e4();
      FUN_0800a014();
      FUN_0803ebd0(0x7d);
    } while (iVar13 != 8);
LAB_08015c9c:
    FUN_0802f42c();
    iVar13 = 3;
    iVar5 = FUN_0802c818(9);
  }
  if (iVar5 != 0) {
    FUN_0800a6e4();
    FUN_08009fbc(DAT_08015e8c);
    FUN_0803ebd0(2000);
    iVar5 = FUN_0801e07c();
    if (iVar5 != 0) {
      FUN_080265d8();
    }
    FUN_0803ebd0(2000);
  }
  iVar5 = FUN_0802c818(7);
  puVar16 = DAT_08015e7c;
  if (iVar5 == 0) {
    FUN_080277ac(DAT_08015af8);
    iVar5 = FUN_0802c818(0);
  }
  else {
    iVar5 = 0;
    FUN_08009fbc();
    FUN_08009bcc(DAT_08015e80);
    FUN_080225a4(DAT_08015e80);
    do {
      if (iVar5 << 0x1f < 0) {
        FUN_0800a6e4();
      }
      else {
        FUN_0800a60c(*puVar16);
      }
      iVar5 = iVar5 + 1;
      FUN_0800a014();
      FUN_0803ebd0(0x7d);
    } while (iVar5 != 5);
    FUN_0800a6e4();
    FUN_0800a014();
    iVar5 = FUN_0802c818(0);
  }
  if (((iVar5 == 0) || (*(char *)(iVar7 + 0xb1) == '\0')) ||
     (*(undefined *)(iVar7 + 0xb1) = 0, *(int *)(iVar7 + 0xa8) == 0)) {
    iVar5 = FUN_0802c818(1);
  }
  else {
    local_128 = local_128 & 0xffffff00;
    (**(code **)(iVar7 + 0xac))(DAT_08015e84,&local_128);
    iVar5 = FUN_0802c818(1);
  }
  if (((iVar5 == 0) || (*(char *)(iVar7 + 0xb1) == '\x01')) ||
     (*(undefined *)(iVar7 + 0xb1) = 1, *(int *)(iVar7 + 0xa8) == 0)) {
    iVar5 = FUN_0802c818(2);
  }
  else {
    local_128._1_3_ = (undefined3)(local_128 >> 8);
    local_128 = CONCAT31(local_128._1_3_,1);
    (**(code **)(iVar7 + 0xac))(DAT_08015e84,&local_128);
    iVar5 = FUN_0802c818(2);
  }
  if (((iVar5 == 0) || (*(char *)(iVar7 + 0xb1) == '\x02')) ||
     (*(undefined *)(iVar7 + 0xb1) = 2, *(int *)(iVar7 + 0xa8) == 0)) {
    iVar5 = FUN_0802c818(3);
  }
  else {
    local_128._1_3_ = (undefined3)(local_128 >> 8);
    local_128 = CONCAT31(local_128._1_3_,2);
    (**(code **)(iVar7 + 0xac))(DAT_08015e84,&local_128);
    iVar5 = FUN_0802c818(3);
  }
  if (((iVar5 != 0) && (*(char *)(iVar7 + 0xb1) != '\x03')) &&
     (*(undefined *)(iVar7 + 0xb1) = 3, *(int *)(iVar7 + 0xa8) != 0)) {
    local_128._1_3_ = (undefined3)(local_128 >> 8);
    local_128 = CONCAT31(local_128._1_3_,3);
    (**(code **)(iVar7 + 0xac))(DAT_08015e84,&local_128);
  }
  FUN_08009fbc(DAT_08015afc);
  piVar1 = DAT_08015b00;
  *DAT_08015b00 = iVar13;
  piVar3 = DAT_08015e94;
  ppiVar2 = DAT_08015e90;
  if (iVar13 == 2) {
    FUN_0803288c();
  }
  else if (iVar13 == 3) {
    FUN_0803e3b0();
  }
  else if ((iVar13 == 0) && (*DAT_08015e90 != DAT_08015e94)) {
    (**(code **)(**DAT_08015e90 + 0xc))();
    *ppiVar2 = piVar3;
    FUN_08032904(piVar3);
  }
  iVar13 = *(int *)(iVar7 + 0x2c);
  uVar6 = iVar13 + 1;
  *(uint *)(iVar7 + 0x2c) = uVar6;
  if (*(int *)(iVar7 + 0x24) != 0) {
    local_128 = uVar6;
    (**(code **)(iVar7 + 0x28))(DAT_08015b04,&local_128);
  }
  puVar16 = DAT_08015b08;
  FUN_0801e064(iVar13);
  FUN_0804cb60(DAT_08015b0c);
  iVar13 = DAT_08015b14;
  FUN_0804cb68(DAT_08015b10,*puVar16);
  uVar4 = FUN_08045af4();
  FUN_0804cb68(DAT_08015b18,uVar4);
  FUN_0803ebd0(100);
  *(undefined4 *)(iVar13 + 0xa3c) = 0x3f000000;
  *(undefined4 *)(iVar13 + 0xa4c) = 0x3f000000;
  *(undefined4 *)(iVar13 + 0xa50) = 0x3f000000;
  *(undefined4 *)(iVar13 + 0xa38) = 0x3f000000;
  FUN_08056428(iVar13 + 0x334,0,0x34);
  *(undefined4 *)(iVar13 + 0x368) = 0x3f800000;
  if ((0 < (int)*(uint *)(iVar13 + 0x30c)) && ((*(uint *)(iVar13 + 0x30c) & 0x3fffffff) != 0)) {
    FUN_08056428(*(undefined4 *)(iVar13 + 0x308),0);
  }
  *(undefined4 *)(iVar13 + 0x330) = 1;
  FUN_0803ebd0(100);
  FUN_08012fb4();
  FUN_08012c54(*(undefined *)(iVar7 + 0x14),0);
  iVar7 = FUN_0801e07c();
  pcVar11 = DAT_08015b20;
  if (iVar7 == 0) {
    puVar17 = &DAT_00004f80 + (int)DAT_08015b1c;
    puVar14 = DAT_08015b1c;
    do {
      while( true ) {
        puVar16 = (undefined4 *)(puVar14 + -4);
        puVar8 = puVar14 + -4;
        if (*(code **)*puVar16 == pcVar11) break;
        puVar14 = puVar14 + 0x9f0;
        (**(code **)*puVar16)(puVar8,1);
        if (puVar14 == puVar17) goto LAB_08015aa4;
      }
      if ((puVar14[0x11] != '\x01') && (puVar14[0x11] = 1, *(int *)(puVar14 + 8) != 0)) {
        local_128 = CONCAT31(local_128._1_3_,1);
        (**(code **)(puVar14 + 0xc))(puVar14,&local_128);
      }
      puVar14 = puVar14 + 0x9f0;
    } while (puVar14 != puVar17);
  }
LAB_08015aa4:
  FUN_0803ebd0(1000);
  FUN_0802a2c4();
  FUN_0803ebd0(100);
  FUN_08008058(DAT_08015b24);
  FUN_08008bc8(DAT_08015b28);
  *(undefined *)(piVar1 + 2) = 1;
  *(undefined *)(piVar1 + 4) = 1;
  return;
}


```

---
## callers of `0x0801e104` (FUN_0801e104)

### `FUN_08024b00` @ `08024b00`
```c

byte FUN_08024b00(uint param_1)

{
  uint *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  byte bVar8;
  int iVar9;
  undefined4 *puVar10;
  int iVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  undefined4 *puVar15;
  int iVar16;
  byte local_5117;
  char local_5116;
  byte local_5115;
  undefined4 local_5114 [3];
  undefined4 local_5108;
  undefined local_5100;
  undefined4 local_50fc;
  undefined4 local_50f0;
  undefined local_50e8;
  undefined4 local_50e4;
  undefined4 local_50d8;
  undefined auStack_50d0 [72];
  undefined auStack_5088 [304];
  undefined4 local_4f58;
  undefined4 local_4f4c;
  undefined local_4f44;
  undefined4 local_4f40;
  undefined4 local_4f34;
  undefined local_4f2c;
  undefined4 local_4f28;
  undefined4 local_4f1c;
  undefined local_4f14;
  undefined4 local_4f10;
  undefined4 local_4f04;
  undefined local_4efc;
  undefined4 local_4ef8;
  undefined4 local_4eec;
  undefined4 local_4ee4;
  undefined4 uStack_4ee0;
  undefined4 local_4ed4;
  undefined4 local_4ecc;
  undefined4 uStack_4ec8;
  undefined4 local_4ebc;
  undefined4 local_4eb4;
  undefined4 uStack_4eb0;
  undefined4 local_4ea4;
  undefined4 local_4e9c;
  undefined4 uStack_4e98;
  undefined4 local_4e8c;
  undefined local_4e84;
  undefined4 local_4e80;
  undefined4 local_4e74;
  undefined auStack_4e6c [72];
  undefined auStack_4e24 [304];
  undefined4 local_4cf4;
  undefined4 local_4ce8;
  undefined local_4ce0;
  undefined4 local_4cdc;
  undefined4 local_4cd0;
  undefined local_4cc8;
  undefined4 local_4cc4;
  undefined4 local_4cb8;
  undefined local_4cb0;
  undefined4 local_4cac;
  undefined4 local_4ca0;
  undefined local_4c98;
  undefined4 local_4c94;
  undefined4 local_4c88;
  undefined4 local_4c80;
  undefined4 local_4c7c;
  undefined4 local_4c70;
  undefined4 local_4c68;
  undefined4 local_4c64;
  undefined4 local_4c58;
  undefined4 local_4c50;
  undefined4 local_4c4c;
  undefined4 local_4c40;
  undefined4 local_4c38;
  undefined4 local_4c34;
  undefined4 local_4c28;
  undefined local_4c20;
  undefined4 local_4c1c;
  undefined4 local_4c10;
  undefined4 local_4c08;
  undefined4 local_4c04;
  undefined4 local_4bf8;
  undefined4 local_4bf0;
  undefined4 local_4bec;
  undefined4 local_4be0;
  undefined4 local_4bd8;
  undefined4 local_4bd4;
  undefined4 local_4bc8;
  undefined2 local_4bc0;
  undefined4 local_4bbc;
  undefined4 local_4bb0;
  undefined4 local_4ba8;
  undefined4 local_4ba4;
  undefined4 local_4b98;
  undefined4 local_4b90;
  undefined4 local_4b8c;
  undefined4 local_4b80;
  undefined local_4b78;
  undefined4 local_4b74;
  undefined4 local_4b68;
  undefined auStack_4b60 [256];
  undefined4 local_4a60;
  undefined4 local_4a54;
  undefined auStack_4a4c [256];
  undefined4 local_494c;
  undefined4 local_4940;
  undefined auStack_4938 [256];
  undefined4 local_4838;
  undefined4 local_482c;
  undefined4 local_4824;
  undefined4 local_4820;
  undefined4 local_4814;
  undefined4 local_480c;
  undefined4 local_4808;
  undefined4 local_4804;
  undefined4 local_4800;
  undefined4 local_47fc;
  undefined4 local_47f0;
  undefined4 local_47e8;
  undefined4 local_47e4;
  undefined4 local_47d8;
  undefined4 local_47d0;
  undefined4 local_47cc;
  undefined4 local_47c0;
  undefined4 local_47b8;
  undefined4 local_47b4;
  undefined4 local_47a8;
  undefined4 local_47a0;
  undefined4 local_479c;
  undefined4 local_4790;
  undefined local_4788;
  undefined4 local_4784;
  undefined4 local_4778;
  undefined local_4770;
  undefined4 local_476c;
  undefined4 local_4760;
  undefined local_4758;
  undefined4 local_4754;
  undefined4 local_4748;
  undefined4 local_4740;
  undefined4 local_473c;
  undefined4 local_4730;
  undefined4 local_4728;
  undefined4 local_4724;
  undefined4 local_4718;
  undefined local_4710;
  undefined4 local_470c;
  undefined4 local_4700;
  undefined local_46f8;
  undefined4 local_46f4;
  undefined4 local_46e8;
  undefined auStack_46e0 [72];
  undefined auStack_4698 [304];
  undefined4 local_4568;
  undefined4 local_455c;
  undefined local_4554;
  undefined4 local_4550;
  undefined4 local_4544;
  undefined local_453c;
  undefined4 local_4538;
  undefined4 local_452c;
  undefined local_4524;
  undefined4 local_4520;
  undefined4 local_4514;
  undefined local_450c;
  undefined4 local_4508;
  undefined4 local_44fc;
  undefined4 local_44f4;
  undefined4 local_44f0;
  undefined4 local_44e4;
  undefined4 local_44dc;
  undefined4 local_44d8;
  undefined4 local_44cc;
  undefined4 local_44c4;
  undefined4 local_44c0;
  undefined4 local_44b4;
  undefined4 local_44ac;
  undefined4 local_44a8;
  undefined4 local_449c;
  undefined local_4494;
  undefined4 local_4490;
  undefined4 local_4484;
  undefined auStack_447c [72];
  undefined auStack_4434 [304];
  undefined4 local_4304;
  undefined4 local_42f8;
  undefined local_42f0;
  undefined4 local_42ec;
  undefined4 local_42e0;
  undefined local_42d8;
  undefined4 local_42d4;
  undefined4 local_42c8;
  undefined local_42c0;
  undefined4 local_42bc;
  undefined4 local_42b0;
  undefined local_42a8;
  undefined4 local_42a4;
  undefined4 local_4298;
  undefined4 local_4290;
  undefined4 local_428c;
  undefined4 local_4280;
  undefined4 local_4278;
  undefined4 local_4274;
  undefined4 local_4268;
  undefined4 local_4260;
  undefined4 local_425c;
  undefined4 local_4250;
  undefined4 local_4248;
  undefined4 local_4244;
  undefined4 local_4238;
  undefined local_4230;
  undefined4 local_422c;
  undefined4 local_4220;
  undefined4 local_4218;
  undefined4 local_4214;
  undefined4 local_4208;
  undefined4 local_4200;
  undefined4 local_41fc;
  undefined4 local_41f0;
  undefined4 local_41e8;
  undefined4 local_41e4;
  undefined4 local_41d8;
  undefined2 local_41d0;
  undefined4 local_41cc;
  undefined4 local_41c0;
  undefined4 local_41b8;
  undefined4 local_41b4;
  undefined4 local_41a8;
  undefined4 local_41a0;
  undefined4 local_419c;
  undefined4 local_4190;
  undefined local_4188;
  undefined4 local_4184;
  undefined4 local_4178;
  undefined auStack_4170 [256];
  undefined4 local_4070;
  undefined4 local_4064;
  undefined auStack_405c [256];
  undefined4 local_3f5c;
  undefined4 local_3f50;
  undefined auStack_3f48 [256];
  undefined4 local_3e48;
  undefined4 local_3e3c;
  undefined4 local_3e34;
  undefined4 local_3e30;
  undefined4 local_3e24;
  undefined4 local_3e1c;
  undefined4 local_3e18;
  undefined4 local_3e14;
  undefined4 local_3e10;
  undefined4 local_3e0c;
  undefined4 local_3e00;
  undefined4 local_3df8;
  undefined4 local_3df4;
  undefined4 local_3de8;
  undefined4 local_3de0;
  undefined4 local_3ddc;
  undefined4 local_3dd0;
  undefined4 local_3dc8;
  undefined4 local_3dc4;
  undefined4 local_3db8;
  undefined4 local_3db0;
  undefined4 uStack_3dac;
  undefined4 local_3da0;
  undefined local_3d98;
  undefined4 local_3d94;
  undefined4 local_3d88;
  undefined local_3d80;
  undefined4 local_3d7c;
  undefined4 local_3d70;
  undefined local_3d68;
  undefined4 local_3d64;
  undefined4 local_3d58;
  undefined4 local_3d50;
  undefined4 uStack_3d4c;
  undefined4 local_3d40;
  undefined4 local_3d38;
  undefined4 uStack_3d34;
  undefined4 local_3d28;
  undefined local_3d20;
  undefined4 local_3d1c;
  undefined4 local_3d10;
  undefined local_3d08;
  undefined4 local_3d04;
  undefined4 local_3cf8;
  undefined auStack_3cf0 [72];
  undefined auStack_3ca8 [304];
  undefined4 local_3b78;
  undefined4 local_3b6c;
  undefined local_3b64;
  undefined4 local_3b60;
  undefined4 local_3b54;
  undefined local_3b4c;
  undefined4 local_3b48;
  undefined4 local_3b3c;
  undefined local_3b34;
  undefined4 local_3b30;
  undefined4 local_3b24;
  undefined local_3b1c;
  undefined4 local_3b18;
  undefined4 local_3b0c;
  undefined4 local_3b04;
  undefined4 local_3b00;
  undefined4 local_3af4;
  undefined4 local_3aec;
  undefined4 local_3ae8;
  undefined4 local_3adc;
  undefined4 local_3ad4;
  undefined4 local_3ad0;
  undefined4 local_3ac4;
  undefined4 local_3abc;
  undefined4 local_3ab8;
  undefined4 local_3aac;
  undefined local_3aa4;
  undefined4 local_3aa0;
  undefined4 local_3a94;
  undefined auStack_3a8c [72];
  undefined auStack_3a44 [304];
  undefined4 local_3914;
  undefined4 local_3908;
  undefined local_3900;
  undefined4 local_38fc;
  undefined4 local_38f0;
  undefined local_38e8;
  undefined4 local_38e4;
  undefined4 local_38d8;
  undefined local_38d0;
  undefined4 local_38cc;
  undefined4 local_38c0;
  undefined local_38b8;
  undefined4 local_38b4;
  undefined4 local_38a8;
  undefined4 local_38a0;
  undefined4 local_389c;
  undefined4 local_3890;
  undefined4 local_3888;
  undefined4 local_3884;
  undefined4 local_3878;
  undefined4 local_3870;
  undefined4 local_386c;
  undefined4 local_3860;
  undefined4 local_3858;
  undefined4 local_3854;
  undefined4 local_3848;
  undefined local_3840;
  undefined4 local_383c;
  undefined4 local_3830;
  undefined4 local_3828;
  undefined4 local_3824;
  undefined4 local_3818;
  undefined4 local_3810;
  undefined4 local_380c;
  undefined4 local_3800;
  undefined4 local_37f8;
  undefined4 local_37f4;
  undefined4 local_37e8;
  undefined2 local_37e0;
  undefined4 local_37dc;
  undefined4 local_37d0;
  undefined4 local_37c8;
  undefined4 local_37c4;
  undefined4 local_37b8;
  undefined4 local_37b0;
  undefined4 local_37ac;
  undefined4 local_37a0;
  undefined local_3798;
  undefined4 local_3794;
  undefined4 local_3788;
  undefined auStack_3780 [256];
  undefined4 local_3680;
  undefined4 local_3674;
  undefined auStack_366c [256];
  undefined4 local_356c;
  undefined4 local_3560;
  undefined auStack_3558 [256];
  undefined4 local_3458;
  undefined4 local_344c;
  undefined4 local_3444;
  undefined4 local_3440;
  undefined4 local_3434;
  undefined4 local_342c;
  undefined4 local_3428;
  undefined4 local_3424;
  undefined4 local_3420;
  undefined4 local_341c;
  undefined4 local_3410;
  undefined4 local_3408;
  undefined4 local_3404;
  undefined4 local_33f8;
  undefined4 local_33f0;
  undefined4 local_33ec;
  undefined4 local_33e0;
  undefined4 local_33d8;
  undefined4 local_33d4;
  undefined4 local_33c8;
  undefined4 local_33c0;
  undefined4 local_33bc;
  undefined4 local_33b0;
  undefined local_33a8;
  undefined4 local_33a4;
  undefined4 local_3398;
  undefined local_3390;
  undefined4 local_338c;
  undefined4 local_3380;
  undefined local_3378;
  undefined4 local_3374;
  undefined4 local_3368;
  undefined4 local_3360;
  undefined4 local_335c;
  undefined4 local_3350;
  undefined4 local_3348;
  undefined4 local_3344;
  undefined4 local_3338;
  undefined local_3330;
  undefined4 local_332c;
  undefined4 local_3320;
  undefined local_3318;
  undefined4 local_3314;
  undefined4 local_3308;
  undefined auStack_3300 [72];
  undefined auStack_32b8 [304];
  undefined4 local_3188;
  undefined4 local_317c;
  undefined local_3174;
  undefined4 local_3170;
  undefined4 local_3164;
  undefined local_315c;
  undefined4 local_3158;
  undefined4 local_314c;
  undefined local_3144;
  undefined4 local_3140;
  undefined4 local_3134;
  undefined local_312c;
  undefined4 local_3128;
  undefined4 local_311c;
  undefined4 local_3114;
  undefined4 local_3110;
  undefined4 local_3104;
  undefined4 local_30fc;
  undefined4 local_30f8;
  undefined4 local_30ec;
  undefined4 local_30e4;
  undefined4 local_30e0;
  undefined4 local_30d4;
  undefined4 local_30cc;
  undefined4 local_30c8;
  undefined4 local_30bc;
  undefined local_30b4;
  undefined4 local_30b0;
  undefined4 local_30a4;
  undefined auStack_309c [72];
  undefined auStack_3054 [304];
  undefined4 local_2f24;
  undefined4 local_2f18;
  undefined local_2f10;
  undefined4 local_2f0c;
  undefined4 local_2f00;
  undefined local_2ef8;
  undefined4 local_2ef4;
  undefined4 local_2ee8;
  undefined local_2ee0;
  undefined4 local_2edc;
  undefined4 local_2ed0;
  undefined local_2ec8;
  undefined4 local_2ec4;
  undefined4 local_2eb8;
  undefined4 local_2eb0;
  undefined4 uStack_2eac;
  undefined4 local_2ea0;
  undefined4 local_2e98;
  undefined4 uStack_2e94;
  undefined4 local_2e88;
  undefined4 local_2e80;
  undefined4 uStack_2e7c;
  undefined4 local_2e70;
  undefined4 local_2e68;
  undefined4 uStack_2e64;
  undefined4 local_2e58;
  undefined local_2e50;
  undefined4 local_2e4c;
  undefined4 local_2e40;
  undefined4 local_2e38;
  undefined4 local_2e34;
  undefined4 local_2e28;
  undefined4 local_2e20;
  undefined4 local_2e1c;
  undefined4 local_2e10;
  undefined4 local_2e08;
  undefined4 local_2e04;
  undefined4 local_2df8;
  undefined2 local_2df0;
  undefined4 local_2dec;
  undefined4 local_2de0;
  undefined4 local_2dd8;
  undefined4 local_2dd4;
  undefined4 local_2dc8;
  undefined4 local_2dc0;
  undefined4 local_2dbc;
  undefined4 local_2db0;
  undefined local_2da8;
  undefined4 local_2da4;
  undefined4 local_2d98;
  undefined auStack_2d90 [256];
  undefined4 local_2c90;
  undefined4 local_2c84;
  undefined auStack_2c7c [256];
  undefined4 local_2b7c;
  undefined4 local_2b70;
  undefined auStack_2b68 [256];
  undefined4 local_2a68;
  undefined4 local_2a5c;
  undefined4 local_2a54;
  undefined4 local_2a50;
  undefined4 local_2a44;
  undefined4 local_2a3c;
  undefined4 local_2a38;
  undefined4 local_2a34;
  undefined4 local_2a30;
  undefined4 local_2a2c;
  undefined4 local_2a20;
  undefined4 local_2a18;
  undefined4 local_2a14;
  undefined4 local_2a08;
  undefined4 local_2a00;
  undefined4 local_29fc;
  undefined4 local_29f0;
  undefined4 local_29e8;
  undefined4 local_29e4;
  undefined4 local_29d8;
  undefined4 local_29d0;
  undefined4 local_29cc;
  undefined4 local_29c0;
  undefined local_29b8;
  undefined4 local_29b4;
  undefined4 local_29a8;
  undefined local_29a0;
  undefined4 local_299c;
  undefined4 local_2990;
  undefined local_2988;
  undefined4 local_2984;
  undefined4 local_2978;
  undefined4 local_2970;
  undefined4 local_296c;
  undefined4 local_2960;
  undefined4 local_2958;
  undefined4 local_2954;
  undefined4 local_2948;
  undefined local_2940;
  undefined4 local_293c;
  undefined4 local_2930;
  undefined local_2928;
  undefined4 local_2924;
  undefined4 local_2918;
  undefined auStack_2910 [72];
  undefined auStack_28c8 [304];
  undefined4 local_2798;
  undefined4 local_278c;
  undefined local_2784;
  undefined4 local_2780;
  undefined4 local_2774;
  undefined local_276c;
  undefined4 local_2768;
  undefined4 local_275c;
  undefined local_2754;
  undefined4 local_2750;
  undefined4 local_2744;
  undefined local_273c;
  undefined4 local_2738;
  undefined4 local_272c;
  undefined4 local_2724;
  undefined4 local_2720;
  undefined4 local_2714;
  undefined4 local_270c;
  undefined4 local_2708;
  undefined4 local_26fc;
  undefined4 local_26f4;
  undefined4 local_26f0;
  undefined4 local_26e4;
  undefined4 local_26dc;
  undefined4 local_26d8;
  undefined4 local_26cc;
  undefined local_26c4;
  undefined4 local_26c0;
  undefined4 local_26b4;
  undefined auStack_26ac [72];
  undefined auStack_2664 [304];
  undefined4 local_2534;
  undefined4 local_2528;
  undefined local_2520;
  undefined4 local_251c;
  undefined4 local_2510;
  undefined local_2508;
  undefined4 local_2504;
  undefined4 local_24f8;
  undefined local_24f0;
  undefined4 local_24ec;
  undefined4 local_24e0;
  undefined local_24d8;
  undefined4 local_24d4;
  undefined4 local_24c8;
  undefined4 local_24c0;
  undefined4 local_24bc;
  undefined4 local_24b0;
  undefined4 local_24a8;
  undefined4 local_24a4;
  undefined4 local_2498;
  undefined4 local_2490;
  undefined4 local_248c;
  undefined4 local_2480;
  undefined4 local_2478;
  undefined4 local_2474;
  undefined4 local_2468;
  undefined local_2460;
  undefined4 local_245c;
  undefined4 local_2450;
  undefined4 local_2448;
  undefined4 local_2444;
  undefined4 local_2438;
  undefined4 local_2430;
  undefined4 local_242c;
  undefined4 local_2420;
  undefined4 local_2418;
  undefined4 local_2414;
  undefined4 local_2408;
  undefined2 local_2400;
  undefined4 local_23fc;
  undefined4 local_23f0;
  undefined4 local_23e8;
  undefined4 local_23e4;
  undefined4 local_23d8;
  undefined4 local_23d0;
  undefined4 local_23cc;
  undefined4 local_23c0;
  undefined local_23b8;
  undefined4 local_23b4;
  undefined4 local_23a8;
  undefined auStack_23a0 [256];
  undefined4 local_22a0;
  undefined4 local_2294;
  undefined auStack_228c [256];
  undefined4 local_218c;
  undefined4 local_2180;
  undefined auStack_2178 [256];
  undefined4 local_2078;
  undefined4 local_206c;
  undefined4 local_2064;
  undefined4 local_2060;
  undefined4 local_2054;
  undefined4 local_204c;
  undefined4 local_2048;
  undefined4 local_2044;
  undefined4 local_2040;
  undefined4 local_203c;
  undefined4 local_2030;
  undefined4 local_2028;
  undefined4 local_2024;
  undefined4 local_2018;
  undefined4 local_2010;
  undefined4 local_200c;
  undefined4 local_2000;
  undefined4 local_1ff8;
  undefined4 local_1ff4;
  undefined4 local_1fe8;
  undefined4 local_1fe0;
  undefined4 uStack_1fdc;
  undefined4 local_1fd0;
  undefined local_1fc8;
  undefined4 local_1fc4;
  undefined4 local_1fb8;
  undefined local_1fb0;
  undefined4 local_1fac;
  undefined4 local_1fa0;
  undefined local_1f98;
  undefined4 local_1f94;
  undefined4 local_1f88;
  undefined4 local_1f80;
  undefined4 uStack_1f7c;
  undefined4 local_1f70;
  undefined4 local_1f68;
  undefined4 uStack_1f64;
  undefined4 local_1f58;
  undefined local_1f50;
  undefined4 local_1f4c;
  undefined4 local_1f40;
  undefined local_1f38;
  undefined4 local_1f34;
  undefined4 local_1f28;
  undefined auStack_1f20 [72];
  undefined auStack_1ed8 [304];
  undefined4 local_1da8;
  undefined4 local_1d9c;
  undefined local_1d94;
  undefined4 local_1d90;
  undefined4 local_1d84;
  undefined local_1d7c;
  undefined4 local_1d78;
  undefined4 local_1d6c;
  undefined local_1d64;
  undefined4 local_1d60;
  undefined4 local_1d54;
  undefined local_1d4c;
  undefined4 local_1d48;
  undefined4 local_1d3c;
  undefined4 local_1d34;
  undefined4 uStack_1d30;
  undefined4 local_1d24;
  undefined4 local_1d1c;
  undefined4 uStack_1d18;
  undefined4 local_1d0c;
  undefined4 local_1d04;
  undefined4 uStack_1d00;
  undefined4 local_1cf4;
  undefined4 local_1cec;
  undefined4 uStack_1ce8;
  undefined4 local_1cdc;
  undefined local_1cd4;
  undefined4 local_1cd0;
  undefined4 local_1cc4;
  undefined auStack_1cbc [72];
  undefined auStack_1c74 [304];
  undefined4 local_1b44;
  undefined4 local_1b38;
  undefined local_1b30;
  undefined4 local_1b2c;
  undefined4 local_1b20;
  undefined local_1b18;
  undefined4 local_1b14;
  undefined4 local_1b08;
  undefined local_1b00;
  undefined4 local_1afc;
  undefined4 local_1af0;
  undefined local_1ae8;
  undefined4 local_1ae4;
  undefined4 local_1ad8;
  undefined4 local_1ad0;
  undefined4 local_1acc;
  undefined4 local_1ac0;
  undefined4 local_1ab8;
  undefined4 local_1ab4;
  undefined4 local_1aa8;
  undefined4 local_1aa0;
  undefined4 local_1a9c;
  undefined4 local_1a90;
  undefined4 local_1a88;
  undefined4 local_1a84;
  undefined4 local_1a78;
  undefined local_1a70;
  undefined4 local_1a6c;
  undefined4 local_1a60;
  undefined4 local_1a58;
  undefined4 local_1a54;
  undefined4 local_1a48;
  undefined4 local_1a40;
  undefined4 local_1a3c;
  undefined4 local_1a30;
  undefined4 local_1a28;
  undefined4 local_1a24;
  undefined4 local_1a18;
  undefined2 local_1a10;
  undefined4 local_1a0c;
  undefined4 local_1a00;
  undefined4 local_19f8;
  undefined4 local_19f4;
  undefined4 local_19e8;
  undefined4 local_19e0;
  undefined4 local_19dc;
  undefined4 local_19d0;
  undefined local_19c8;
  undefined4 local_19c4;
  undefined4 local_19b8;
  undefined auStack_19b0 [256];
  undefined4 local_18b0;
  undefined4 local_18a4;
  undefined auStack_189c [256];
  undefined4 local_179c;
  undefined4 local_1790;
  undefined auStack_1788 [256];
  undefined4 local_1688;
  undefined4 local_167c;
  undefined4 local_1674;
  undefined4 local_1670;
  undefined4 local_1664;
  undefined4 local_165c;
  undefined4 local_1658;
  undefined4 local_1654;
  undefined4 local_1650;
  undefined4 local_164c;
  undefined4 local_1640;
  undefined4 local_1638;
  undefined4 local_1634;
  undefined4 local_1628;
  undefined4 local_1620;
  undefined4 local_161c;
  undefined4 local_1610;
  undefined4 local_1608;
  undefined4 local_1604;
  undefined4 local_15f8;
  undefined4 local_15f0;
  undefined4 local_15ec;
  undefined4 local_15e0;
  undefined local_15d8;
  undefined4 local_15d4;
  undefined4 local_15c8;
  undefined local_15c0;
  undefined4 local_15bc;
  undefined4 local_15b0;
  undefined local_15a8;
  undefined4 local_15a4;
  undefined4 local_1598;
  undefined4 local_1590;
  undefined4 local_158c;
  undefined4 local_1580;
  undefined4 local_1578;
  undefined4 local_1574;
  undefined4 local_1568;
  undefined local_1560;
  undefined4 local_155c;
  undefined4 local_1550;
  undefined local_1548;
  undefined4 local_1544;
  undefined4 local_1538;
  undefined auStack_1530 [72];
  undefined auStack_14e8 [304];
  undefined4 local_13b8;
  undefined4 local_13ac;
  undefined local_13a4;
  undefined4 local_13a0;
  undefined4 local_1394;
  undefined local_138c;
  undefined4 local_1388;
  undefined4 local_137c;
  undefined local_1374;
  undefined4 local_1370;
  undefined4 local_1364;
  undefined local_135c;
  undefined4 local_1358;
  undefined4 local_134c;
  undefined4 local_1344;
  undefined4 local_1340;
  undefined4 local_1334;
  undefined4 local_132c;
  undefined4 local_1328;
  undefined4 local_131c;
  undefined4 local_1314;
  undefined4 local_1310;
  undefined4 local_1304;
  undefined4 local_12fc;
  undefined4 local_12f8;
  undefined4 local_12ec;
  undefined local_12e4;
  undefined4 local_12e0;
  undefined4 local_12d4;
  undefined auStack_12cc [72];
  undefined auStack_1284 [304];
  undefined4 local_1154;
  undefined4 local_1148;
  undefined local_1140;
  undefined4 local_113c;
  undefined4 local_1130;
  undefined local_1128;
  undefined4 local_1124;
  undefined4 local_1118;
  undefined local_1110;
  undefined4 local_110c;
  undefined4 local_1100;
  undefined local_10f8;
  undefined4 local_10f4;
  undefined4 local_10e8;
  undefined4 local_10e0;
  undefined4 local_10dc;
  undefined4 local_10d0;
  undefined4 local_10c8;
  undefined4 local_10c4;
  undefined4 local_10b8;
  undefined4 local_10b0;
  undefined4 local_10ac;
  undefined4 local_10a0;
  undefined4 local_1098;
  undefined4 local_1094;
  undefined4 local_1088;
  undefined local_1080;
  undefined4 local_107c;
  undefined4 local_1070;
  undefined4 local_1068;
  undefined4 local_1064;
  undefined4 local_1058;
  undefined4 local_1050;
  undefined4 local_104c;
  undefined4 local_1040;
  undefined4 local_1038;
  undefined4 local_1034;
  undefined4 local_1028;
  undefined2 local_1020;
  undefined4 local_101c;
  undefined4 local_1010;
  undefined4 local_1008;
  undefined4 local_1004;
  undefined4 local_ff8;
  undefined4 local_ff0;
  undefined4 local_fec;
  undefined4 local_fe0;
  undefined local_fd8;
  undefined4 local_fd4;
  undefined4 local_fc8;
  undefined auStack_fc0 [256];
  undefined4 local_ec0;
  undefined4 local_eb4;
  undefined auStack_eac [256];
  undefined4 local_dac;
  undefined4 local_da0;
  undefined auStack_d98 [256];
  undefined4 local_c98;
  undefined4 local_c8c;
  undefined4 local_c84;
  undefined4 local_c80;
  undefined4 local_c74;
  undefined4 local_c6c;
  undefined4 local_c68;
  undefined4 local_c64;
  undefined4 local_c60;
  undefined4 local_c5c;
  undefined4 local_c50;
  undefined4 local_c48;
  undefined4 local_c44;
  undefined4 local_c38;
  undefined4 local_c30;
  undefined4 local_c2c;
  undefined4 local_c20;
  undefined4 local_c18;
  undefined4 local_c14;
  undefined4 local_c08;
  undefined4 local_c00;
  undefined4 local_bfc;
  undefined4 local_bf0;
  undefined local_be8;
  undefined4 local_be4;
  undefined4 local_bd8;
  undefined local_bd0;
  undefined4 local_bcc;
  undefined4 local_bc0;
  undefined local_bb8;
  undefined4 local_bb4;
  undefined4 local_ba8;
  undefined4 local_ba0;
  undefined4 local_b9c;
  undefined4 local_b90;
  undefined4 local_b88;
  undefined4 local_b84;
  undefined4 local_b78;
  undefined local_b70;
  undefined4 local_b6c;
  undefined4 local_b60;
  undefined local_b58;
  undefined4 local_b54;
  undefined4 local_b48;
  undefined auStack_b40 [72];
  undefined auStack_af8 [304];
  undefined4 local_9c8;
  undefined4 local_9bc;
  undefined local_9b4;
  undefined4 local_9b0;
  undefined4 local_9a4;
  undefined local_99c;
  undefined4 local_998;
  undefined4 local_98c;
  undefined local_984;
  undefined4 local_980;
  undefined4 local_974;
  undefined local_96c;
  undefined4 local_968;
  undefined4 local_95c;
  undefined4 local_954;
  undefined4 local_950;
  undefined4 local_944;
  undefined4 local_93c;
  undefined4 local_938;
  undefined4 local_92c;
  undefined4 local_924;
  undefined4 local_920;
  undefined4 local_914;
  undefined4 local_90c;
  undefined4 local_908;
  undefined4 local_8fc;
  undefined local_8f4;
  undefined4 local_8f0;
  undefined4 local_8e4;
  undefined auStack_8dc [72];
  undefined auStack_894 [304];
  undefined4 local_764;
  undefined4 local_758;
  undefined local_750;
  undefined4 local_74c;
  undefined4 local_740;
  undefined local_738;
  undefined4 local_734;
  undefined4 local_728;
  undefined local_720;
  undefined4 local_71c;
  undefined4 local_710;
  undefined local_708;
  undefined4 local_704;
  undefined4 local_6f8;
  undefined4 local_6f0;
  undefined4 local_6ec;
  undefined4 local_6e0;
  undefined4 local_6d8;
  undefined4 local_6d4;
  undefined4 local_6c8;
  undefined4 local_6c0;
  undefined4 local_6bc;
  undefined4 local_6b0;
  undefined4 local_6a8;
  undefined4 local_6a4;
  undefined4 local_698;
  undefined local_690;
  undefined4 local_68c;
  undefined4 local_680;
  undefined4 local_678;
  undefined4 local_674;
  undefined4 local_668;
  undefined4 local_660;
  undefined4 local_65c;
  undefined4 local_650;
  undefined4 local_648;
  undefined4 local_644;
  undefined4 local_638;
  undefined2 local_630;
  undefined4 local_62c;
  undefined4 local_620;
  undefined4 local_618;
  undefined4 local_614;
  undefined4 local_608;
  undefined4 local_600;
  undefined4 local_5fc;
  undefined4 local_5f0;
  undefined local_5e8;
  undefined4 local_5e4;
  undefined4 local_5d8;
  undefined auStack_5d0 [256];
  undefined4 local_4d0;
  undefined4 local_4c4;
  undefined auStack_4bc [256];
  undefined4 local_3bc;
  undefined4 local_3b0;
  undefined auStack_3a8 [256];
  undefined4 local_2a8;
  undefined4 local_29c;
  undefined4 local_294;
  undefined4 local_290;
  undefined4 local_284;
  undefined4 local_27c;
  undefined4 local_278;
  undefined4 local_274;
  undefined4 local_270;
  undefined4 local_26c;
  undefined4 local_260;
  undefined4 local_258;
  undefined4 local_254;
  undefined4 local_248;
  undefined4 local_240;
  undefined4 local_23c;
  undefined4 local_230;
  undefined4 local_228;
  undefined4 local_224;
  undefined4 local_218;
  undefined4 local_210;
  undefined4 local_20c;
  undefined4 local_200;
  undefined local_1f8;
  undefined4 local_1f4;
  undefined4 local_1e8;
  undefined local_1e0;
  undefined4 local_1dc;
  undefined4 local_1d0;
  undefined local_1c8;
  undefined4 local_1c4;
  undefined4 local_1b8;
  undefined4 local_1b0;
  undefined4 local_1ac;
  undefined4 local_1a0;
  undefined4 local_198;
  undefined4 local_194;
  undefined auStack_190 [8];
  code *local_188;
  code *local_184;
  byte local_180;
  undefined4 local_17c;
  undefined auStack_178 [8];
  code *local_170;
  undefined local_168;
  undefined4 local_164;
  undefined auStack_160 [8];
  code *local_158;
  undefined local_150;
  undefined auStack_14c [8];
  code *local_144;
  undefined4 local_13c;
  undefined local_138;
  undefined4 local_134;
  undefined auStack_130 [8];
  code *local_128;
  undefined4 local_120;
  undefined4 local_11c;
  undefined auStack_118 [8];
  code *local_110;
  undefined4 local_108;
  undefined4 local_104;
  undefined auStack_100 [8];
  code *local_f8;
  undefined local_f0;
  undefined4 local_ec;
  undefined auStack_e8 [8];
  code *local_e0;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined auStack_d0 [8];
  code *local_c8;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined auStack_b8 [8];
  code *local_b0;
  undefined4 local_a8;
  undefined auStack_a4 [8];
  code *local_9c;
  undefined4 local_94;
  undefined2 local_90;
  undefined local_8e;
  undefined4 local_8c;
  undefined auStack_88 [8];
  code *local_80;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined auStack_64 [8];
  code *local_5c;
  undefined4 local_54;
  undefined4 local_50;
  undefined auStack_4c [8];
  code *local_44;
  undefined4 local_3c;
  undefined4 uStack_38;
  
  uVar2 = DAT_08024b94;
  puVar1 = DAT_08024b90;
  if (*DAT_08024b8c == 3) {
    return 1;
  }
  if (0x2f < param_1) {
    return 9;
  }
  *DAT_08024b8c = 1;
  FUN_0804cb58(uVar2);
  if (*puVar1 != param_1) {
    FUN_080569f8(DAT_08024b9c,DAT_08024b98,param_1 + 1);
    uVar3 = DAT_08024ba0;
    uVar2 = DAT_08024b9c;
    *puVar1 = param_1;
    FUN_0804cb68(uVar3,uVar2);
    FUN_08051058(DAT_08024ba8,DAT_08024ba4,1);
    bVar8 = FUN_0805253c(DAT_08024b9c);
    if ((bVar8 & 0xf7) == 0) {
      bVar8 = FUN_0801f448();
    }
    if (bVar8 != 0) {
      if (bVar8 != 1) {
        if (bVar8 == 0x12) {
          iVar9 = 2;
        }
        else {
          iVar9 = 0;
        }
        *DAT_08024b8c = iVar9;
        return bVar8;
      }
      *DAT_080265b4 = 3;
      return 1;
    }
  }
  uVar4 = DAT_08024f54;
  uVar3 = DAT_08024f50;
  uVar2 = DAT_08024f4c;
  local_5108 = 0;
  local_5100 = 0;
  local_50f0 = 0;
  puVar10 = (undefined4 *)((int)&uStack_38 + DAT_08024f48);
  local_50e8 = 0;
  local_50d8 = 0;
  local_50e4 = DAT_08024f50;
  local_5114[0] = DAT_08024f4c;
  local_50fc = DAT_08024f4c;
  FUN_08056428(auStack_50d0,0,0x48);
  uVar6 = DAT_08024f8c;
  FUN_08016170(auStack_5088);
  uVar7 = DAT_08024f90;
  uVar5 = DAT_08024f58;
  local_4f4c = 0;
  local_4f44 = 0;
  local_4f34 = 0;
  local_4f2c = 0;
  local_4f1c = 0;
  local_4f14 = 0;
  local_4f04 = 0;
  local_4efc = 0;
  local_4eec = 0;
  local_4ed4 = 0;
  local_4ebc = 0;
  local_4ea4 = 0;
  local_4e8c = 0;
  local_4e84 = 0;
  local_4e80 = uVar3;
  local_4e74 = 0;
  local_4f58 = uVar2;
  local_4f40 = uVar2;
  local_4f28 = uVar2;
  local_4f10 = uVar2;
  local_4ef8 = uVar4;
  local_4ee4 = 0;
  uStack_4ee0 = uVar4;
  local_4ecc = 0;
  uStack_4ec8 = uVar4;
  local_4eb4 = 0;
  uStack_4eb0 = uVar4;
  local_4e9c = 0;
  uStack_4e98 = uVar2;
  FUN_08056428(auStack_4e6c,0,0x48);
  FUN_08016170(auStack_4e24);
  local_4ce8 = 0;
  local_4ce0 = 0;
  local_4cd0 = 0;
  local_4cc8 = 0;
  local_4cb8 = 0;
  local_4cb0 = 0;
  local_4ca0 = 0;
  local_4c98 = 0;
  local_4c88 = 0;
  local_4c80 = 0;
  local_4c70 = 0;
  local_4c68 = 0;
  local_4c58 = 0;
  local_4c50 = 0;
  local_4c40 = 0;
  local_4c38 = 0;
  local_4c28 = 0;
  local_4c20 = 0;
  local_4c10 = 0;
  local_4bf8 = 0;
  local_4c08 = 0x1000000;
  local_4c1c = DAT_08024f60;
  local_4c04 = DAT_08024f64;
  local_4cf4 = uVar2;
  local_4cdc = uVar2;
  local_4cc4 = uVar2;
  local_4cac = uVar2;
  local_4c94 = uVar4;
  local_4c7c = uVar4;
  local_4c64 = uVar4;
  local_4c4c = uVar4;
  local_4c34 = uVar2;
  local_4bf0 = uVar6;
  local_4bbc = DAT_08024f5c;
  local_4ba4 = DAT_08024f5c;
  local_4bec = DAT_08024f68;
  local_4b90 = uVar5;
  local_4bd4 = DAT_08024f6c;
  local_4b8c = DAT_08024f70;
  local_4ba8 = uVar5;
  local_4be0 = 0;
  local_4bd8 = uVar6;
  local_4bc8 = 0;
  local_4bc0 = 0;
  local_4bb0 = 0;
  local_4b98 = 0;
  local_4b80 = 0;
  local_4b78 = 0;
  local_4b74 = uVar7;
  local_4b68 = 0;
  FUN_08056428(auStack_4b60,0,0x100);
  local_4a60 = uVar7;
  local_4a54 = 0;
  FUN_08056428(auStack_4a4c,0,0x100);
  local_494c = uVar7;
  local_4940 = 0;
  FUN_08056428(auStack_4938,0,0x100);
  local_4820 = DAT_08024f74;
  local_4838 = DAT_08024f78;
  local_47fc = DAT_08024f7c;
  local_47cc = DAT_08024f80;
  local_47e4 = DAT_08024f84;
  local_47b4 = DAT_08024f88;
  local_4808 = uVar5;
  local_4800 = 0x3f800000;
  local_4804 = 0xbf800000;
  local_482c = 0;
  local_4824 = 0x1000000;
  local_4814 = 0;
  local_47f0 = 0;
  local_47e8 = 0x1000000;
  local_47d8 = 0;
  local_47d0 = 0x1000000;
  local_47c0 = 0;
  local_47b8 = 0x1000000;
  local_47a8 = 0;
  local_47a0 = uVar6;
  local_4790 = 0;
  local_4788 = 0;
  local_4778 = 0;
  local_4770 = 0;
  local_4760 = 0;
  local_4758 = 0;
  local_4748 = 0;
  local_480c = uVar5;
  local_479c = uVar2;
  local_4784 = uVar2;
  local_476c = uVar2;
  local_4754 = uVar4;
  local_4740 = 0;
  local_4730 = 0;
  local_4728 = 0;
  local_4718 = 0;
  local_4710 = 0;
  local_4700 = 0;
  local_46f8 = 0;
  local_46f4 = uVar3;
  local_46e8 = 0;
  local_473c = uVar4;
  local_4724 = uVar2;
  local_470c = uVar2;
  FUN_08056428(auStack_46e0,0,0x48);
  FUN_08016170(auStack_4698);
  local_455c = 0;
  local_4554 = 0;
  local_4544 = 0;
  local_453c = 0;
  local_452c = 0;
  local_4524 = 0;
  local_4514 = 0;
  local_450c = 0;
  local_44fc = 0;
  local_44f4 = 0;
  local_44e4 = 0;
  local_44dc = 0;
  local_44cc = 0;
  local_44c4 = 0;
  local_44b4 = 0;
  local_44ac = 0;
  local_449c = 0;
  local_4494 = 0;
  local_4490 = uVar3;
  local_4484 = 0;
  local_4568 = uVar2;
  local_4550 = uVar2;
  local_4538 = uVar2;
  local_4520 = uVar2;
  local_4508 = uVar4;
  local_44f0 = uVar4;
  local_44d8 = uVar4;
  local_44c0 = uVar4;
  local_44a8 = uVar2;
  FUN_08056428(auStack_447c,0,0x48);
  uVar3 = DAT_08024f60;
  FUN_08016170(auStack_4434);
  local_42f8 = 0;
  local_42f0 = 0;
  local_42e0 = 0;
  local_42d8 = 0;
  local_42c8 = 0;
  local_42c0 = 0;
  local_42b0 = 0;
  local_42a8 = 0;
  local_4298 = 0;
  local_4290 = 0;
  local_4280 = 0;
  local_4278 = 0;
  local_4268 = 0;
  local_4260 = 0;
  local_4250 = 0;
  local_4248 = 0;
  local_4238 = 0;
  local_4230 = 0;
  local_422c = uVar3;
  local_4220 = 0;
  local_4218 = 0x1000000;
  local_4214 = DAT_08024f64;
  local_4208 = 0;
  local_4304 = uVar2;
  local_42ec = uVar2;
  local_42d4 = uVar2;
  local_42bc = uVar2;
  local_42a4 = uVar4;
  local_428c = uVar4;
  local_4274 = uVar4;
  local_425c = uVar4;
  local_4244 = uVar2;
  local_4200 = uVar6;
  local_41fc = DAT_08024f68;
  local_41cc = DAT_08024f5c;
  local_41b4 = DAT_08024f5c;
  local_419c = DAT_08024f70;
  local_41b8 = uVar5;
  local_41a0 = uVar5;
  local_41f0 = 0;
  local_41e8 = uVar6;
  local_41e4 = DAT_0802539c;
  local_41d8 = 0;
  local_41d0 = 0;
  local_41c0 = 0;
  local_41a8 = 0;
  local_4190 = 0;
  local_4188 = 0;
  local_4184 = uVar7;
  local_4178 = 0;
  FUN_08056428(auStack_4170,0,0x100);
  local_4070 = uVar7;
  local_4064 = 0;
  FUN_08056428(auStack_405c,0,0x100);
  local_3f5c = uVar7;
  local_3f50 = 0;
  FUN_08056428(auStack_3f48,0,0x100);
  local_3e48 = DAT_080253a0;
  local_3e30 = DAT_080253a4;
  local_3e0c = DAT_080253a8;
  local_3dc4 = DAT_080253ac;
  local_3e3c = 0;
  local_3e34 = 0x1000000;
  local_3e24 = 0;
  local_3e00 = 0;
  local_3df8 = 0x1000000;
  local_3df4 = DAT_080253b0;
  local_3de8 = 0;
  local_3de0 = 0x1000000;
  local_3ddc = DAT_080253b4;
  local_3dd0 = 0;
  local_3dc8 = 0x1000000;
  local_3db8 = 0;
  local_3da0 = 0;
  local_3d98 = 0;
  local_3d88 = 0;
  local_3d80 = 0;
  local_3d70 = 0;
  local_3d68 = 0;
  local_3d58 = 0;
  local_3e1c = uVar5;
  local_3e18 = uVar5;
  local_3e14 = 0xbf800000;
  local_3e10 = 0x3f800000;
  local_3d94 = uVar2;
  local_3d7c = uVar2;
  local_3d64 = uVar4;
  local_3db0 = uVar6;
  uStack_3dac = uVar2;
  local_3d50 = 0;
  uStack_3d4c = uVar4;
  local_3d40 = 0;
  local_3d28 = 0;
  local_3d20 = 0;
  local_3d10 = 0;
  local_3d08 = 0;
  local_3d04 = DAT_080253b8;
  local_3cf8 = 0;
  local_3d1c = uVar2;
  local_3d38 = 0;
  uStack_3d34 = uVar2;
  FUN_08056428(auStack_3cf0,0,0x48);
  FUN_08016170(auStack_3ca8);
  local_3b6c = 0;
  local_3b64 = 0;
  local_3b54 = 0;
  local_3b4c = 0;
  local_3b3c = 0;
  local_3b34 = 0;
  local_3b24 = 0;
  local_3b1c = 0;
  local_3b0c = 0;
  local_3b04 = 0;
  local_3af4 = 0;
  local_3aec = 0;
  local_3adc = 0;
  local_3ad4 = 0;
  local_3ac4 = 0;
  local_3abc = 0;
  local_3aac = 0;
  local_3aa4 = 0;
  local_3aa0 = DAT_080253b8;
  local_3a94 = 0;
  local_3b78 = uVar2;
  local_3b60 = uVar2;
  local_3b48 = uVar2;
  local_3b30 = uVar2;
  local_3b18 = uVar4;
  local_3b00 = uVar4;
  local_3ae8 = uVar4;
  local_3ad0 = uVar4;
  local_3ab8 = uVar2;
  FUN_08056428(auStack_3a8c,0,0x48);
  FUN_08016170(auStack_3a44);
  local_3908 = 0;
  local_3900 = 0;
  local_38f0 = 0;
  local_38e8 = 0;
  local_38d8 = 0;
  local_38d0 = 0;
  local_38c0 = 0;
  local_38b8 = 0;
  local_38a8 = 0;
  local_38a0 = 0;
  local_3890 = 0;
  local_3888 = 0;
  local_3878 = 0;
  local_3870 = 0;
  local_3860 = 0;
  local_3858 = 0;
  local_3848 = 0;
  local_3840 = 0;
  local_383c = DAT_080253bc;
  local_3830 = 0;
  local_3828 = 0x1000000;
  local_3824 = DAT_080253c0;
  local_3818 = 0;
  local_3914 = uVar2;
  local_38fc = uVar2;
  local_38e4 = uVar2;
  local_38cc = uVar2;
  local_38b4 = uVar4;
  local_389c = uVar4;
  local_3884 = uVar4;
  local_386c = uVar4;
  local_3854 = uVar2;
  local_3810 = uVar6;
  local_380c = DAT_080253c4;
  local_37ac = DAT_080253cc;
  local_3800 = 0;
  local_37f8 = uVar6;
  local_37f4 = DAT_0802539c;
  local_37e8 = 0;
  local_37e0 = 0;
  local_37dc = DAT_080253c8;
  local_37d0 = 0;
  local_37c4 = DAT_080253c8;
  local_37b8 = 0;
  local_37a0 = 0;
  local_3798 = 0;
  local_3794 = uVar7;
  local_3788 = 0;
  local_37c8 = uVar5;
  local_37b0 = uVar5;
  FUN_08056428(auStack_3780,0,0x100);
  local_3680 = uVar7;
  local_3674 = 0;
  FUN_08056428(auStack_366c,0,0x100);
  local_356c = uVar7;
  local_3560 = 0;
  FUN_08056428(auStack_3558,0,0x100);
  local_3458 = DAT_080253a0;
  local_3440 = DAT_080253a4;
  local_341c = DAT_080253a8;
  local_3404 = DAT_080253b0;
  local_33ec = DAT_080253b4;
  local_33d4 = DAT_080253ac;
  local_344c = 0;
  local_3444 = 0x1000000;
  local_3434 = 0;
  local_3410 = 0;
  local_3408 = 0x1000000;
  local_33f8 = 0;
  local_33f0 = 0x1000000;
  local_33e0 = 0;
  local_33d8 = 0x1000000;
  local_33c8 = 0;
  local_33c0 = uVar6;
  local_33b0 = 0;
  local_33a8 = 0;
  local_3398 = 0;
  local_3390 = 0;
  local_3380 = 0;
  local_3378 = 0;
  local_3368 = 0;
  local_3428 = uVar5;
  local_33bc = uVar2;
  local_33a4 = uVar2;
  local_338c = uVar2;
  local_3374 = uVar4;
  local_342c = uVar5;
  local_3424 = 0xbf800000;
  local_3420 = 0x3f800000;
  local_3360 = 0;
  local_3350 = 0;
  local_3348 = 0;
  local_3338 = 0;
  local_3330 = 0;
  local_3320 = 0;
  local_3318 = 0;
  local_3314 = DAT_080253b8;
  local_3308 = 0;
  local_335c = uVar4;
  local_3344 = uVar2;
  local_332c = uVar2;
  FUN_08056428(auStack_3300,0,0x48);
  FUN_08016170(auStack_32b8);
  local_317c = 0;
  local_3174 = 0;
  local_3164 = 0;
  local_315c = 0;
  local_314c = 0;
  local_3144 = 0;
  local_3134 = 0;
  local_312c = 0;
  local_311c = 0;
  local_3114 = 0;
  local_3104 = 0;
  local_30fc = 0;
  local_30ec = 0;
  local_30e4 = 0;
  local_30d4 = 0;
  local_30cc = 0;
  local_30bc = 0;
  local_30b4 = 0;
  local_30b0 = DAT_080257bc;
  local_30a4 = 0;
  local_3188 = uVar2;
  local_3170 = uVar2;
  local_3158 = uVar2;
  local_3140 = uVar2;
  local_3128 = uVar4;
  local_3110 = uVar4;
  local_30f8 = uVar4;
  local_30e0 = uVar4;
  local_30c8 = uVar2;
  FUN_08056428(auStack_309c,0,0x48);
  FUN_08016170(auStack_3054);
  local_2e4c = DAT_080257c0;
  local_2e34 = DAT_080257c4;
  local_2f18 = 0;
  local_2f10 = 0;
  local_2f00 = 0;
  local_2ef8 = 0;
  local_2ee8 = 0;
  local_2ee0 = 0;
  local_2ed0 = 0;
  local_2ec8 = 0;
  local_2eb8 = 0;
  local_2ea0 = 0;
  local_2e88 = 0;
  local_2e70 = 0;
  local_2e58 = 0;
  local_2e50 = 0;
  local_2e40 = 0;
  local_2e38 = 0x1000000;
  local_2e28 = 0;
  local_2f24 = uVar2;
  local_2f0c = uVar2;
  local_2ef4 = uVar2;
  local_2edc = uVar2;
  local_2ec4 = uVar4;
  local_2eb0 = 0;
  uStack_2eac = uVar4;
  local_2e98 = 0;
  uStack_2e94 = uVar4;
  local_2e80 = 0;
  uStack_2e7c = uVar4;
  local_2e68 = 0;
  uStack_2e64 = uVar2;
  local_2e20 = uVar6;
  local_2e1c = DAT_080257c8;
  local_2e10 = 0;
  local_2e08 = uVar6;
  local_2e04 = DAT_080257d0;
  local_2df8 = 0;
  local_2df0 = 0;
  local_2dec = DAT_080257cc;
  local_2de0 = 0;
  local_2dd4 = DAT_080257cc;
  local_2dc8 = 0;
  local_2dbc = DAT_080257d4;
  local_2db0 = 0;
  local_2da8 = 0;
  local_2da4 = uVar7;
  local_2d98 = 0;
  local_2dd8 = uVar5;
  local_2dc0 = uVar5;
  FUN_08056428(auStack_2d90,0,0x100);
  local_2c90 = uVar7;
  local_2c84 = 0;
  FUN_08056428(auStack_2c7c,0,0x100);
  local_2b7c = uVar7;
  local_2b70 = 0;
  FUN_08056428(auStack_2b68,0,0x100);
  local_2a68 = DAT_080257d8;
  local_2a50 = DAT_080257dc;
  local_2a2c = DAT_080257e0;
  local_2a14 = DAT_080257e4;
  local_29fc = DAT_080257e8;
  local_29e4 = DAT_080257ec;
  local_2a34 = 0xbf800000;
  local_2a5c = 0;
  local_2a54 = 0x1000000;
  local_2a44 = 0;
  local_2a20 = 0;
  local_2a18 = 0x1000000;
  local_2a08 = 0;
  local_2a00 = 0x1000000;
  local_29f0 = 0;
  local_29e8 = 0x1000000;
  local_29d8 = 0;
  local_29d0 = uVar6;
  local_29c0 = 0;
  local_29b8 = 0;
  local_29a8 = 0;
  local_29a0 = 0;
  local_2990 = 0;
  local_2988 = 0;
  local_2978 = 0;
  local_29cc = uVar2;
  local_29b4 = uVar2;
  local_299c = uVar2;
  local_2984 = uVar4;
  local_2a3c = uVar5;
  local_2a38 = uVar5;
  local_2a30 = 0x3f800000;
  local_2970 = 0;
  local_2960 = 0;
  local_2958 = 0;
  local_2948 = 0;
  local_2940 = 0;
  local_2930 = 0;
  local_2928 = 0;
  local_2924 = DAT_080257bc;
  local_2918 = 0;
  local_296c = uVar4;
  local_2954 = uVar2;
  local_293c = uVar2;
  FUN_08056428(auStack_2910,0,0x48);
  FUN_08016170(auStack_28c8);
  local_278c = 0;
  local_2784 = 0;
  local_2774 = 0;
  local_276c = 0;
  local_275c = 0;
  local_2754 = 0;
  local_2744 = 0;
  local_273c = 0;
  local_272c = 0;
  local_2724 = 0;
  local_2714 = 0;
  local_270c = 0;
  local_26fc = 0;
  local_26f4 = 0;
  local_26e4 = 0;
  local_26dc = 0;
  local_26cc = 0;
  local_26c4 = 0;
  local_26c0 = DAT_080257bc;
  local_26b4 = 0;
  local_2798 = uVar2;
  local_2780 = uVar2;
  local_2768 = uVar2;
  local_2750 = uVar2;
  local_2738 = uVar4;
  local_2720 = uVar4;
  local_2708 = uVar4;
  local_26f0 = uVar4;
  local_26d8 = uVar2;
  FUN_08056428(auStack_26ac,0,0x48);
  FUN_08016170(auStack_2664);
  local_2528 = 0;
  local_2520 = 0;
  local_2510 = 0;
  local_2508 = 0;
  local_24f8 = 0;
  local_24f0 = 0;
  local_24e0 = 0;
  local_24d8 = 0;
  local_24c8 = 0;
  local_24c0 = 0;
  local_24b0 = 0;
  local_24a8 = 0;
  local_2498 = 0;
  local_2490 = 0;
  local_2480 = 0;
  local_2478 = 0;
  local_2468 = 0;
  local_2460 = 0;
  local_245c = DAT_080257c0;
  local_2450 = 0;
  local_2448 = 0x1000000;
  local_2444 = DAT_080257c4;
  local_2438 = 0;
  local_2534 = uVar2;
  local_251c = uVar2;
  local_2504 = uVar2;
  local_24ec = uVar2;
  local_24d4 = uVar4;
  local_24bc = uVar4;
  local_24a4 = uVar4;
  local_248c = uVar4;
  local_2474 = uVar2;
  local_2430 = uVar6;
  local_242c = DAT_080257c8;
  local_23fc = DAT_080257cc;
  local_23e4 = DAT_080257cc;
  local_2420 = 0;
  local_2418 = uVar6;
  local_2414 = DAT_080257d0;
  local_2408 = 0;
  local_2400 = 0;
  local_23f0 = 0;
  local_23d8 = 0;
  local_23cc = DAT_080257d4;
  local_23c0 = 0;
  local_23b8 = 0;
  local_23b4 = uVar7;
  local_23a8 = 0;
  local_23e8 = uVar5;
  local_23d0 = uVar5;
  FUN_08056428(auStack_23a0,0,0x100);
  local_22a0 = uVar7;
  local_2294 = 0;
  FUN_08056428(auStack_228c,0,0x100);
  local_218c = uVar7;
  local_2180 = 0;
  FUN_08056428(auStack_2178,0,0x100);
  uVar3 = DAT_08025c40;
  local_2078 = DAT_08025c28;
  local_2060 = DAT_08025c2c;
  local_206c = 0;
  local_2064 = 0x1000000;
  local_2054 = 0;
  local_203c = DAT_08025c30;
  local_2024 = DAT_08025c34;
  local_200c = DAT_08025c38;
  local_1ff4 = DAT_08025c3c;
  local_2048 = uVar5;
  local_2030 = 0;
  local_2028 = 0x1000000;
  local_2018 = 0;
  local_2010 = 0x1000000;
  local_2000 = 0;
  local_1ff8 = 0x1000000;
  local_1fe8 = 0;
  local_1fd0 = 0;
  local_1fc8 = 0;
  local_1fb8 = 0;
  local_1fb0 = 0;
  local_1fa0 = 0;
  local_1f98 = 0;
  local_1f88 = 0;
  local_1fc4 = uVar2;
  local_1fac = uVar2;
  local_1f94 = uVar4;
  local_204c = uVar5;
  local_2044 = 0xbf800000;
  local_2040 = 0x3f800000;
  local_1fe0 = uVar6;
  uStack_1fdc = uVar2;
  local_1f80 = 0;
  uStack_1f7c = uVar4;
  local_1f70 = 0;
  local_1f58 = 0;
  local_1f50 = 0;
  local_1f40 = 0;
  local_1f38 = 0;
  local_1f34 = DAT_08025c40;
  local_1f28 = 0;
  local_1f4c = uVar2;
  local_1f68 = 0;
  uStack_1f64 = uVar2;
  FUN_08056428(auStack_1f20,0,0x48);
  FUN_08016170(auStack_1ed8);
  local_1d9c = 0;
  local_1d94 = 0;
  local_1d84 = 0;
  local_1d7c = 0;
  local_1d6c = 0;
  local_1d64 = 0;
  local_1d54 = 0;
  local_1d4c = 0;
  local_1d3c = 0;
  local_1d24 = 0;
  local_1d0c = 0;
  local_1cf4 = 0;
  local_1cdc = 0;
  local_1cd4 = 0;
  local_1cd0 = uVar3;
  local_1cc4 = 0;
  local_1da8 = uVar2;
  local_1d90 = uVar2;
  local_1d78 = uVar2;
  local_1d60 = uVar2;
  local_1d48 = uVar4;
  local_1d34 = 0;
  uStack_1d30 = uVar4;
  local_1d1c = 0;
  uStack_1d18 = uVar4;
  local_1d04 = 0;
  uStack_1d00 = uVar4;
  local_1cec = 0;
  uStack_1ce8 = uVar2;
  FUN_08056428(auStack_1cbc,0,0x48);
  FUN_08016170(auStack_1c74);
  local_1b38 = 0;
  local_1b30 = 0;
  local_1b20 = 0;
  local_1b18 = 0;
  local_1b08 = 0;
  local_1b00 = 0;
  local_1af0 = 0;
  local_1ae8 = 0;
  local_1ad8 = 0;
  local_1ad0 = 0;
  local_1ac0 = 0;
  local_1ab8 = 0;
  local_1aa8 = 0;
  local_1aa0 = 0;
  local_1a90 = 0;
  local_1a88 = 0;
  local_1a78 = 0;
  local_1a70 = 0;
  local_1a6c = DAT_08025c44;
  local_1a60 = 0;
  local_1a58 = 0x1000000;
  local_1a54 = DAT_08025c48;
  local_1a48 = 0;
  local_1b44 = uVar2;
  local_1b2c = uVar2;
  local_1b14 = uVar2;
  local_1afc = uVar2;
  local_1ae4 = uVar4;
  local_1acc = uVar4;
  local_1ab4 = uVar4;
  local_1a9c = uVar4;
  local_1a84 = uVar2;
  local_1a40 = uVar6;
  local_1a3c = DAT_08025c4c;
  local_1a24 = DAT_08025c54;
  local_1a0c = DAT_08025c50;
  local_19f4 = DAT_08025c50;
  local_19e0 = uVar5;
  local_1a30 = 0;
  local_1a28 = uVar6;
  local_1a18 = 0;
  local_1a10 = 0;
  local_1a00 = 0;
  local_19e8 = 0;
  local_19dc = DAT_08025c58;
  local_19d0 = 0;
  local_19c8 = 0;
  local_19c4 = uVar7;
  local_19b8 = 0;
  local_19f8 = uVar5;
  FUN_08056428(auStack_19b0,0,0x100);
  local_18b0 = uVar7;
  local_18a4 = 0;
  FUN_08056428(auStack_189c,0,0x100);
  local_179c = uVar7;
  local_1790 = 0;
  FUN_08056428(auStack_1788,0,0x100);
  local_1688 = DAT_08025c28;
  local_1670 = DAT_08025c2c;
  local_164c = DAT_08025c30;
  local_1634 = DAT_08025c34;
  local_161c = DAT_08025c38;
  local_1604 = DAT_08025c3c;
  local_165c = uVar5;
  local_167c = 0;
  local_1674 = 0x1000000;
  local_1664 = 0;
  local_1640 = 0;
  local_1638 = 0x1000000;
  local_1628 = 0;
  local_1620 = 0x1000000;
  local_1610 = 0;
  local_1608 = 0x1000000;
  local_15f8 = 0;
  local_15f0 = uVar6;
  local_15e0 = 0;
  local_15d8 = 0;
  local_15c8 = 0;
  local_15c0 = 0;
  local_15b0 = 0;
  local_15a8 = 0;
  local_1598 = 0;
  local_15ec = uVar2;
  local_15d4 = uVar2;
  local_15bc = uVar2;
  local_15a4 = uVar4;
  local_1658 = uVar5;
  local_1654 = 0xbf800000;
  local_1650 = 0x3f800000;
  local_1590 = 0;
  local_1580 = 0;
  local_1578 = 0;
  local_1568 = 0;
  local_1560 = 0;
  local_1550 = 0;
  local_1548 = 0;
  local_1544 = uVar3;
  local_1538 = 0;
  local_158c = uVar4;
  local_1574 = uVar2;
  local_155c = uVar2;
  FUN_08056428(auStack_1530,0,0x48);
  FUN_08016170(auStack_14e8);
  local_13ac = 0;
  local_13a4 = 0;
  local_1394 = 0;
  local_138c = 0;
  local_137c = 0;
  local_1374 = 0;
  local_1364 = 0;
  local_135c = 0;
  local_134c = 0;
  local_1344 = 0;
  local_1334 = 0;
  local_132c = 0;
  local_131c = 0;
  local_1314 = 0;
  local_1304 = 0;
  local_12fc = 0;
  local_12ec = 0;
  local_12e4 = 0;
  local_12e0 = uVar3;
  local_12d4 = 0;
  local_13b8 = uVar2;
  local_13a0 = uVar2;
  local_1388 = uVar2;
  local_1370 = uVar2;
  local_1358 = uVar4;
  local_1340 = uVar4;
  local_1328 = uVar4;
  local_1310 = uVar4;
  local_12f8 = uVar2;
  FUN_08056428(auStack_12cc,0,0x48);
  FUN_08016170(auStack_1284);
  local_107c = DAT_08026028;
  local_1148 = 0;
  local_1140 = 0;
  local_1130 = 0;
  local_1128 = 0;
  local_1118 = 0;
  local_1110 = 0;
  local_1100 = 0;
  local_10f8 = 0;
  local_10e8 = 0;
  local_10e0 = 0;
  local_10d0 = 0;
  local_10c8 = 0;
  local_10b0 = 0;
  local_10a0 = 0;
  local_1098 = 0;
  local_1088 = 0;
  local_1080 = 0;
  local_1070 = 0;
  local_1068 = 0x1000000;
  local_1064 = DAT_0802602c;
  local_1058 = 0;
  local_10b8 = 0;
  local_1154 = uVar2;
  local_113c = uVar2;
  local_1124 = uVar2;
  local_110c = uVar2;
  local_10f4 = uVar4;
  local_10dc = uVar4;
  local_10c4 = uVar4;
  local_10ac = uVar4;
  local_1094 = uVar2;
  local_1050 = uVar6;
  local_104c = DAT_08026030;
  local_1040 = 0;
  local_1038 = uVar6;
  local_1034 = DAT_08026038;
  local_1028 = 0;
  local_1020 = 0;
  local_101c = DAT_08026034;
  local_1010 = 0;
  local_1004 = DAT_08026034;
  local_ff8 = 0;
  local_fec = DAT_0802603c;
  local_fe0 = 0;
  local_fd8 = 0;
  local_fd4 = uVar7;
  local_fc8 = 0;
  local_1008 = uVar5;
  local_ff0 = uVar5;
  FUN_08056428(auStack_fc0,0,0x100);
  local_ec0 = uVar7;
  local_eb4 = 0;
  FUN_08056428(auStack_eac,0,0x100);
  local_dac = uVar7;
  local_da0 = 0;
  FUN_08056428(auStack_d98,0,0x100);
  local_c98 = DAT_08026040;
  local_c80 = DAT_08026044;
  local_c5c = DAT_08026048;
  local_c8c = 0;
  local_c84 = 0x1000000;
  local_c74 = 0;
  local_c50 = 0;
  local_c48 = 0x1000000;
  local_c44 = DAT_0802604c;
  local_c38 = 0;
  local_c30 = 0x1000000;
  local_c2c = DAT_08026050;
  local_c20 = 0;
  local_c18 = 0x1000000;
  local_c14 = DAT_08026054;
  local_c08 = 0;
  local_c00 = uVar6;
  local_bf0 = 0;
  local_be8 = 0;
  local_bd8 = 0;
  local_bd0 = 0;
  local_bc0 = 0;
  local_bb8 = 0;
  local_ba8 = 0;
  local_c6c = uVar5;
  local_c68 = uVar5;
  local_c64 = 0xbf800000;
  local_c60 = 0x3f800000;
  local_bfc = uVar2;
  local_be4 = uVar2;
  local_bcc = uVar2;
  local_bb4 = uVar4;
  local_ba0 = 0;
  local_b54 = DAT_08026058;
  local_b90 = 0;
  local_b88 = 0;
  local_b78 = 0;
  local_b70 = 0;
  local_b60 = 0;
  local_b58 = 0;
  local_b48 = 0;
  local_b9c = uVar4;
  local_b84 = uVar2;
  local_b6c = uVar2;
  FUN_08056428(auStack_b40,0,0x48);
  FUN_08016170(auStack_af8);
  local_9bc = 0;
  local_8f0 = DAT_08026058;
  local_9b4 = 0;
  local_9a4 = 0;
  local_99c = 0;
  local_98c = 0;
  local_984 = 0;
  local_974 = 0;
  local_96c = 0;
  local_95c = 0;
  local_954 = 0;
  local_944 = 0;
  local_93c = 0;
  local_92c = 0;
  local_924 = 0;
  local_914 = 0;
  local_90c = 0;
  local_8fc = 0;
  local_8f4 = 0;
  local_8e4 = 0;
  local_9c8 = uVar2;
  local_9b0 = uVar2;
  local_998 = uVar2;
  local_980 = uVar2;
  local_968 = uVar4;
  local_950 = uVar4;
  local_938 = uVar4;
  local_920 = uVar4;
  local_908 = uVar2;
  FUN_08056428(auStack_8dc,0,0x48);
  FUN_08016170(auStack_894);
  local_674 = DAT_0802602c;
  local_758 = 0;
  local_750 = 0;
  local_740 = 0;
  local_738 = 0;
  local_728 = 0;
  local_720 = 0;
  local_710 = 0;
  local_708 = 0;
  local_6f8 = 0;
  local_6f0 = 0;
  local_6e0 = 0;
  local_6d8 = 0;
  local_6c8 = 0;
  local_6c0 = 0;
  local_6b0 = 0;
  local_6a8 = 0;
  local_698 = 0;
  local_690 = 0;
  local_68c = DAT_08026028;
  local_680 = 0;
  local_678 = 0x1000000;
  local_668 = 0;
  local_764 = uVar2;
  local_74c = uVar2;
  local_734 = uVar2;
  local_71c = uVar2;
  local_704 = uVar4;
  local_6ec = uVar4;
  local_6d4 = uVar4;
  local_6bc = uVar4;
  local_6a4 = uVar2;
  local_660 = uVar6;
  local_65c = DAT_08026030;
  local_5fc = DAT_0802603c;
  local_644 = DAT_08026038;
  local_62c = DAT_08026034;
  local_614 = DAT_08026034;
  local_650 = 0;
  local_648 = uVar6;
  local_638 = 0;
  local_630 = 0;
  local_620 = 0;
  local_608 = 0;
  local_5f0 = 0;
  local_5e8 = 0;
  local_5e4 = uVar7;
  local_5d8 = 0;
  local_618 = uVar5;
  local_600 = uVar5;
  FUN_08056428(auStack_5d0,0,0x100);
  local_4d0 = uVar7;
  local_4c4 = 0;
  FUN_08056428(auStack_4bc,0,0x100);
  local_3bc = uVar7;
  local_3b0 = 0;
  FUN_08056428(auStack_3a8,0,0x100);
  local_2a8 = DAT_08026040;
  local_26c = DAT_08026048;
  local_224 = DAT_080263a4;
  local_210 = uVar6;
  local_254 = DAT_080263a8;
  local_27c = uVar5;
  local_23c = DAT_080263ac;
  local_278 = uVar5;
  local_274 = 0xbf800000;
  local_29c = 0;
  local_294 = 0x1000000;
  local_290 = DAT_080263b0;
  local_284 = 0;
  local_260 = 0;
  local_258 = 0x1000000;
  local_248 = 0;
  local_240 = 0x1000000;
  local_230 = 0;
  local_228 = 0x1000000;
  local_218 = 0;
  local_200 = 0;
  local_1f8 = 0;
  local_1e8 = 0;
  local_1e0 = 0;
  local_1d0 = 0;
  local_1c8 = 0;
  local_1b8 = 0;
  local_270 = 0x3f800000;
  local_20c = uVar2;
  local_1f4 = uVar2;
  local_1dc = uVar2;
  local_1c4 = uVar4;
  local_1b0 = 0;
  local_ec = DAT_080263b4;
  local_138 = 8;
  local_134 = DAT_080263b8;
  local_1a0 = 0;
  local_198 = 0;
  local_188 = (code *)0x0;
  local_180 = 0;
  local_170 = (code *)0x0;
  local_168 = 0;
  local_158 = (code *)0x0;
  local_150 = 0;
  local_144 = (code *)0x0;
  local_13c = 0;
  local_128 = (code *)0x0;
  local_120 = 0x1000000;
  local_110 = (code *)0x0;
  local_108 = 0x1000000;
  local_f8 = (code *)0x0;
  local_f0 = 0;
  local_e0 = (code *)0x0;
  local_d8 = 0x1000000;
  local_c8 = (code *)0x0;
  local_c0 = 0x1000000;
  local_b0 = (code *)0x0;
  local_11c = DAT_080263bc;
  local_d4 = DAT_080263c0;
  local_bc = DAT_080263c4;
  local_1ac = uVar4;
  local_194 = uVar2;
  local_17c = uVar2;
  local_164 = uVar2;
  local_104 = uVar2;
  local_a8 = 0x1000000;
  local_8c = DAT_080263b0;
  local_94 = 0;
  local_78 = uVar5;
  local_9c = (code *)0x0;
  local_90 = 0;
  local_80 = (code *)0x0;
  local_5c = (code *)0x0;
  local_54 = 0;
  local_44 = (code *)0x0;
  local_3c = 0;
  local_5116 = '\0';
  local_74 = uVar5;
  local_70 = 0xff7fffff;
  local_6c = DAT_080263c8;
  local_68 = uVar4;
  local_50 = uVar4;
  local_8e = 0xff;
  FUN_0804cb58(DAT_080263cc);
  local_5117 = FUN_08024414(DAT_080263d0,local_5114);
  if (local_5117 == 0) {
    local_5117 = FUN_0801e104(puVar10,&local_5116);
    if (local_5117 == 0) {
      if (local_5116 != '\0') {
        if (*DAT_080265b4 == 3) {
          local_5117 = 1;
        }
        else {
          local_5117 = FUN_080216f8(DAT_080265b8,puVar10);
        }
      }
      iVar9 = DAT_080265d4;
      if (local_5117 == 0) {
        iVar16 = 1;
        uVar12 = 0;
        do {
          uVar14 = uVar12 >> 5;
          uVar13 = 1 << (uVar12 & 0x1f);
          if ((uVar13 & *(uint *)(iVar9 + uVar14 * 4)) != 0) {
            FUN_0804cb68(DAT_080265bc,iVar16);
            FUN_080569f8(DAT_080265c4,DAT_080265c0,iVar16);
            iVar11 = FUN_08024414(DAT_080265c4,puVar10);
            bVar8 = (byte)uVar12;
            if (((iVar11 == 0) && ((uint)local_180 != (uVar12 & 0xff))) &&
               (local_180 = bVar8, local_188 != (code *)0x0)) {
              local_5115 = bVar8;
              (*local_184)(auStack_190,&local_5115);
            }
            local_5117 = (byte)iVar11;
            if ((local_5117 != 0) ||
               (local_5117 = FUN_0801e104(puVar10,&local_5116), local_5117 != 0)) goto LAB_0802651e;
            if (local_5116 != '\0') {
              if (*DAT_080265d0 < 0x30) {
                FUN_080569f8(DAT_080265c4,DAT_080265c0,iVar16);
                if (*DAT_080265b4 == 3) {
                  iVar11 = 1;
                }
                else {
                  iVar11 = FUN_080216f8(DAT_080265c4,puVar10);
                  if (iVar11 == 0) {
                    if (((uint)local_180 != (uVar12 & 0xff)) &&
                       (local_180 = bVar8, local_188 != (code *)0x0)) {
                      local_5115 = bVar8;
                      (*local_184)(auStack_190,&local_5115);
                    }
                    *(uint *)(iVar9 + uVar14 * 4) = *(uint *)(iVar9 + uVar14 * 4) | uVar13;
                  }
                }
              }
              else {
                iVar11 = 9;
              }
              local_5117 = (byte)iVar11;
            }
            if (local_5117 != 0) goto LAB_0802651e;
            FUN_0804cb68(DAT_080265c8,iVar16);
          }
          uVar12 = uVar12 + 1;
          iVar16 = iVar16 + 1;
        } while (uVar12 != 0x30);
        FUN_0804cb68(DAT_080265cc,param_1 + 1);
      }
LAB_0802651e:
      if (local_5117 != 1) {
        FUN_0801d860(local_5117);
        goto LAB_08026234;
      }
    }
    else if (local_5117 != 1) {
      if (local_5117 != 0x12) {
        *DAT_080265b4 = 0;
        goto LAB_08026234;
      }
      goto LAB_0802642e;
    }
  }
  else if (local_5117 != 1) {
    if (local_5117 != 0x12) {
      *DAT_080263d4 = 0;
      goto LAB_08026234;
    }
LAB_0802642e:
    *DAT_080265b4 = 2;
    local_5117 = 0x12;
    goto LAB_08026234;
  }
  local_5117 = 1;
  *DAT_080265b4 = 3;
LAB_08026234:
  local_50 = uVar4;
  if (local_44 != (code *)0x0) {
    (*local_44)(auStack_4c,auStack_4c,3);
  }
  local_68 = uVar4;
  if (local_5c != (code *)0x0) {
    (*local_5c)(auStack_64,auStack_64,3);
  }
  local_8c = DAT_080263b0;
  if (local_80 != (code *)0x0) {
    (*local_80)(auStack_88,auStack_88,3);
  }
  if (local_9c != (code *)0x0) {
    (*local_9c)(auStack_a4,auStack_a4,3);
  }
  local_bc = DAT_080263c4;
  if (local_b0 != (code *)0x0) {
    (*local_b0)(auStack_b8,auStack_b8,3);
  }
  local_d4 = DAT_080263c0;
  if (local_c8 != (code *)0x0) {
    (*local_c8)(auStack_d0,auStack_d0,3);
  }
  local_ec = DAT_080263b4;
  if (local_e0 != (code *)0x0) {
    (*local_e0)(auStack_e8,auStack_e8,3);
  }
  local_104 = uVar2;
  if (local_f8 != (code *)0x0) {
    (*local_f8)(auStack_100,auStack_100,3);
  }
  local_11c = DAT_080263bc;
  if (local_110 != (code *)0x0) {
    (*local_110)(auStack_118,auStack_118,3);
  }
  local_134 = DAT_080263b8;
  if (local_128 != (code *)0x0) {
    (*local_128)(auStack_130,auStack_130,3);
  }
  if (local_144 != (code *)0x0) {
    (*local_144)(auStack_14c,auStack_14c,3);
  }
  local_164 = uVar2;
  if (local_158 != (code *)0x0) {
    (*local_158)(auStack_160,auStack_160,3);
  }
  local_17c = uVar2;
  if (local_170 != (code *)0x0) {
    (*local_170)(auStack_178,auStack_178,3);
  }
  local_194 = uVar2;
  if (local_188 != (code *)0x0) {
    (*local_188)(auStack_190,auStack_190,3);
  }
  puVar15 = &local_194;
  do {
    puVar15 = puVar15 + -0x27c;
    FUN_08010c78(puVar15);
  } while (puVar15 != puVar10);
  return local_5117;
}


```

### `FUN_080331ac` @ `080331ac`
```c

/* WARNING: Type propagation algorithm not settling */

code ** FUN_080331ac(code **param_1,undefined4 param_2)

{
  uint *puVar1;
  undefined uVar2;
  bool bVar3;
  int **ppiVar4;
  int iVar5;
  code **ppcVar6;
  undefined4 *puVar7;
  int iVar8;
  int iVar9;
  code *pcVar10;
  byte bVar11;
  uint uVar12;
  undefined *puVar13;
  code **ppcVar14;
  char cVar15;
  uint *puVar16;
  code *pcVar17;
  undefined *puVar18;
  uint uVar19;
  byte bVar20;
  int iVar21;
  code **ppcVar22;
  int *piVar23;
  uint *puVar24;
  uint in_fpscr;
  float fVar25;
  undefined local_41;
  float local_40;
  uint local_3c;
  uint local_38;
  code **local_34;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  ppcVar6 = param_1;
  switch(param_2) {
  case 0:
    iVar9 = FUN_080129a8();
    iVar8 = FUN_08012984();
    if (iVar8 == 0) {
      if ((*(uint *)(iVar9 + 0x28) & 0xfffffffd) != 1) goto LAB_08033496;
      if (*(uint *)(iVar9 + 0x28) - 2 < 2) goto switchD_0803320c_caseD_2;
      iVar8 = *(int *)(iVar9 + 0x30);
      *(undefined4 *)(iVar9 + 0x28) = 0;
    }
    else {
      if ((0x12bf < *(int *)(iVar9 + 0x58)) && (*(int *)(iVar9 + 0x28) == 0)) {
LAB_08033496:
        ppcVar6 = (code **)FUN_08010c48();
        ppiVar4 = DAT_0803d590;
        ppcVar22 = DAT_0803d58c;
        DAT_0803d58c[4] = (code *)0x0;
        if (ppcVar6 == (code **)0x0) {
          ppcVar14 = (code **)*ppiVar4;
          ppcVar22[3] = (code *)ppcVar14;
          ppcVar6 = ppcVar14;
        }
        else {
          ppcVar14 = (code **)*ppiVar4;
          ppcVar22[3] = (code *)ppcVar6;
        }
        if (ppcVar14 == ppcVar22) {
          return ppcVar6;
        }
        (**(code **)(*ppcVar14 + 0xc))(ppcVar14);
        *ppiVar4 = (int *)ppcVar22;
        ppcVar6 = DAT_0803d58c;
        iVar9 = FUN_08011344();
        iVar8 = FUN_080129a8();
        FUN_080113fc(0);
        puVar18 = *(undefined **)(iVar8 + 0x34);
        *(undefined2 *)(ppcVar6 + 6) = 0;
        ppcVar6[10] = (code *)0x0;
        ppcVar6[8] = (code *)0x0;
        ppcVar6[9] = (code *)(puVar18 + -1);
        FUN_08056428(&local_40,0,0x28);
        local_2c = *(undefined4 *)(iVar9 + 0x48);
        local_3c = 0x3f800000;
        puVar13 = *(undefined **)(iVar8 + 0x58);
        if (*(char *)(iVar9 + 0x69) == '\x02') {
          local_28 = *(undefined4 *)(iVar9 + 0xf0);
        }
        else {
          local_28 = *(undefined4 *)(iVar9 + 0xcc);
        }
        local_24 = *(undefined4 *)(iVar9 + 0x114);
        local_38 = 0x3f000000;
        if ((int)puVar13 < 0x12c0) {
          puVar13 = puVar18;
          if ((int)puVar18 < 0x12c0) {
            puVar13 = &DAT_000012c0;
          }
          *(uint *)(iVar8 + 0x3c) = (uint)(puVar18 + -0x12c0) & (int)(puVar18 + -0x12c0) >> 0x1f;
        }
        else {
          pcVar17 = (code *)(puVar18 + -(int)puVar13);
          fVar25 = (float)VectorSignedToFloat(puVar18 + -1,(byte)(in_fpscr >> 0x15) & 3);
          ppcVar6[8] = pcVar17;
          local_40 = (float)VectorSignedToFloat(pcVar17,(byte)(in_fpscr >> 0x15) & 3);
          pcVar10 = (code *)(puVar18 + -0x12c0);
          if ((int)pcVar17 <= (int)(puVar18 + -0x12c0)) {
            pcVar10 = pcVar17;
          }
          local_40 = local_40 / fVar25;
          if ((int)puVar18 < (int)puVar13) {
            puVar13 = *(undefined **)(iVar8 + 0x34);
          }
          *(code **)(iVar8 + 0x3c) = pcVar10;
        }
        *(undefined **)(iVar8 + 0x40) = puVar13;
        ppcVar22 = (code **)FUN_0802c464(&local_40,2);
        if ((ppcVar6[4] == (code *)0x0) &&
           (ppcVar22 = (code **)FUN_080129a8(), 0x12bf < (int)ppcVar22[0xd])) {
          switch(*(undefined4 *)(iVar8 + 0x28)) {
          case 0:
          case 1:
          case 5:
            *(undefined4 *)(iVar8 + 0x28) = 0;
            break;
          case 2:
          case 3:
            *(undefined4 *)(iVar8 + 0x28) = 4;
            *(undefined4 *)(iVar8 + 0x5c) = *(undefined4 *)(iVar8 + 0x30);
            break;
          case 6:
            *(undefined4 *)(iVar8 + 0x28) = 7;
          }
          pcVar10 = DAT_0803c7c4;
          FUN_08015ea4(1);
          iVar9 = FUN_0801134c();
          ppcVar22 = *(code ***)(&DAT_00004fe0 + iVar9);
          cVar15 = (&DAT_00004ff5)[iVar9];
          pcVar17 = *ppcVar22;
          *(char *)(ppcVar6 + 0xb) = cVar15;
          if (pcVar17 == pcVar10) {
            if ((cVar15 != '\0') &&
               ((&DAT_00004ff5)[iVar9] = 0, *(int *)(&DAT_00004fec + iVar9) != 0)) {
              local_41 = 0;
              ppcVar22 = (code **)(**(code **)(&DAT_00004ff0 + iVar9))
                                            (&UNK_00004fe4 + iVar9,&local_41);
            }
          }
          else {
            ppcVar22 = (code **)(*pcVar17)(&DAT_00004fe0 + iVar9,0);
          }
        }
        return ppcVar22;
      }
      switch(*(int *)(iVar9 + 0x28)) {
      case 0:
      case 1:
      case 5:
        iVar8 = *(int *)(iVar9 + 0x30);
        *(undefined4 *)(iVar9 + 0x28) = 0;
        break;
      case 2:
      case 3:
switchD_0803320c_caseD_2:
        iVar8 = *(int *)(iVar9 + 0x30);
        *(undefined4 *)(iVar9 + 0x28) = 4;
        *(int *)(iVar9 + 0x5c) = iVar8;
        break;
      default:
        iVar8 = *(int *)(iVar9 + 0x30);
        break;
      case 6:
        iVar8 = *(int *)(iVar9 + 0x30);
        *(undefined4 *)(iVar9 + 0x28) = 7;
      }
    }
    ppcVar6 = *(code ***)(iVar9 + 4);
    iVar8 = iVar8 + *(int *)(iVar9 + 0x18);
    if (iVar8 < (int)ppcVar6) {
      if (iVar8 < 0) {
        iVar8 = iVar8 + (int)ppcVar6;
      }
    }
    else {
      iVar8 = iVar8 - (int)ppcVar6;
    }
    *(int *)(iVar9 + 0x54) = iVar8;
    *(undefined4 *)(iVar9 + 0x58) = *(undefined4 *)(iVar9 + 0x34);
    break;
  case 1:
    iVar9 = FUN_0802c870();
    iVar8 = FUN_080128dc();
    if ((iVar9 < 0) || (iVar8 == 0)) {
      ppcVar6 = (code **)FUN_0801e07c();
      if (ppcVar6 != (code **)0x0) {
        iVar9 = FUN_0801134c();
        uVar2 = (&DAT_00004f94)[iVar9];
        ppcVar6 = (code **)thunk_FUN_0801e0b4(uVar2);
        if (ppcVar6 != (code **)0x0) {
          param_1[9] = (code *)&UNK_00000080;
          ppcVar6 = (code **)FUN_08012b24(uVar2);
          return ppcVar6;
        }
      }
    }
    else {
      iVar9 = FUN_080119dc(iVar9);
      ppcVar6 = (code **)FUN_080119ec(*(char *)(iVar9 + 0x945) == '\x01');
      param_1[7] = (code *)&UNK_00000080;
    }
    break;
  case 2:
    iVar9 = FUN_0802c870();
    iVar8 = FUN_080128dc();
    if ((-1 < iVar9) && (iVar8 != 0)) {
      iVar8 = FUN_080119dc(iVar9);
      FUN_08011ed4(iVar9,*(char *)(iVar8 + 0x945) == '\x01');
      param_1[6] = (code *)&UNK_00000080;
      return (code **)&UNK_00000080;
    }
    iVar9 = FUN_0801134c();
    bVar11 = (&DAT_00004f94)[iVar9];
    uVar19 = (uint)bVar11;
    ppcVar6 = (code **)FUN_0801e07c();
    if (ppcVar6 == (code **)0x0) {
      return (code **)0x0;
    }
    ppcVar6 = (code **)FUN_0801e0dc(uVar19);
    if (ppcVar6 != (code **)0x0) {
      return ppcVar6;
    }
    param_1[8] = (code *)&UNK_00000080;
    iVar8 = DAT_08011488;
    iVar9 = DAT_08011484;
    *(undefined4 *)(DAT_08011488 + 0xc) = 0;
    *(undefined *)(iVar8 + 0x11) = 0;
    FUN_08021bf8(iVar9);
    puVar16 = DAT_08021a18;
    piVar23 = DAT_080219ec;
    iVar9 = DAT_08011484;
    bVar3 = *(char *)(DAT_0801148c + 0x1d1) != '\x01';
    if ((0x2f < uVar19) || (0x2f < *DAT_08021a18)) {
      return (code **)&UNK_00000009;
    }
    if ((1 << (uVar19 & 0x1f) & *(uint *)(DAT_080219e8 + (uint)(bVar11 >> 5) * 4)) != 0) {
      return (code **)&UNK_0000000a;
    }
    local_2c._0_3_ = (uint3)(ushort)local_2c;
    if (bVar3) {
      FUN_080569f8(DAT_080219f4,DAT_080219f0,uVar19 + 1);
      if (*piVar23 == 3) {
        return (code **)&UNK_00000001;
      }
      ppcVar6 = (code **)FUN_080216f8(DAT_080219f4,iVar9);
      if (ppcVar6 != (code **)0x0) {
        return ppcVar6;
      }
LAB_080218e2:
      if (**(code ***)(&DAT_00004f80 + iVar9) == DAT_080219f8) {
        if (((&DAT_00004f94)[iVar9] != bVar11) &&
           ((&DAT_00004f94)[iVar9] = bVar11, *(int *)(&DAT_00004f8c + iVar9) != 0)) {
          local_2c = CONCAT13(bVar11,(uint3)local_2c);
          (**(code **)(&DAT_00004f90 + iVar9))(&UNK_00004f84 + iVar9,(int)&local_2c + 3);
        }
      }
      else {
        (***(code ***)(&DAT_00004f80 + iVar9))(&DAT_00004f80 + iVar9);
      }
      *(uint *)(DAT_080219fc + (uint)(bVar11 >> 5) * 4) =
           1 << (uVar19 & 0x1f) | *(uint *)(DAT_080219fc + (uint)(bVar11 >> 5) * 4);
      if (bVar3) {
        return (code **)0x0;
      }
      ppcVar6 = (code **)0x0;
LAB_0802193e:
      if (local_2c._2_1_ == '\0') {
        return ppcVar6;
      }
      uVar19 = *puVar16;
      FUN_0804cb68(DAT_08021a04,DAT_08021a00);
      if (uVar19 < 0x30) {
        FUN_08051058(DAT_08021a0c,DAT_08021a08,1);
        ppcVar22 = (code **)FUN_0805253c(DAT_08021a00);
        if ((((uint)ppcVar22 & 0xf7) == 0) &&
           (ppcVar22 = (code **)FUN_0801f448(), ppcVar22 == (code **)0x0)) {
          local_38 = *DAT_08021a10;
          puVar24 = DAT_08021a14 + 8;
          local_3c = DAT_08021a10[2] - 1;
          puVar16 = DAT_08021a14;
          local_34 = ppcVar6;
          do {
            iVar21 = iVar9 + 0x7dc;
            puVar1 = puVar16 + 1;
            *puVar1 = 0;
            puVar16[9] = 0;
            puVar16[0x11] = local_3c;
            iVar8 = DAT_08021bf0;
            if (((*(char *)(iVar9 + 0x7dc) != '\0') && (*(char *)(iVar9 + 0x59c) == '\0')) &&
               (0 < (int)local_38)) {
              uVar12 = local_38 & 7;
              uVar19 = 0;
              if (uVar12 == 0) {
LAB_08021b16:
                do {
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x100,iVar21,0x100);
                  uVar12 = uVar19 + 1;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x200,iVar21);
                  uVar12 = uVar19 + 2;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x300,iVar21,0x100);
                  uVar12 = uVar19 + 3;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x400,iVar21,0x100);
                  uVar12 = uVar19 + 4;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x500,iVar21,0x100);
                  uVar12 = uVar19 + 5;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = FUN_08056a38(iVar8 + 0x600,iVar21,0x100);
                  uVar12 = uVar19 + 6;
                  if (iVar5 == 0) goto LAB_08021be2;
                  iVar5 = iVar8 + 0x700;
                  uVar12 = uVar19 + 7;
                  iVar8 = iVar8 + 0x800;
                  iVar5 = FUN_08056a38(iVar5,iVar21,0x100);
                  if (iVar5 == 0) goto LAB_08021be2;
                  uVar19 = uVar19 + 8;
                } while (uVar19 != local_38);
              }
              else {
                if (uVar12 == 1) {
LAB_08021afa:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    if (uVar19 == local_38) goto LAB_08021a1c;
                    goto LAB_08021b16;
                  }
                }
                else if (uVar12 == 2) {
LAB_08021ae4:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    goto LAB_08021afa;
                  }
                }
                else if (uVar12 == 3) {
LAB_08021acc:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    goto LAB_08021ae4;
                  }
                }
                else if (uVar12 == 4) {
LAB_08021ab4:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    goto LAB_08021acc;
                  }
                }
                else if (uVar12 == 5) {
LAB_08021a9c:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    goto LAB_08021ab4;
                  }
                }
                else if (uVar12 == 6) {
LAB_08021a84:
                  iVar5 = FUN_08056a38(iVar8,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    uVar19 = uVar19 + 1;
                    iVar8 = iVar8 + 0x100;
                    goto LAB_08021a9c;
                  }
                }
                else {
                  iVar5 = FUN_08056a38(DAT_08021bf0,iVar21,0x100);
                  uVar12 = uVar19;
                  if (iVar5 != 0) {
                    iVar8 = iVar8 + 0x100;
                    uVar19 = 1;
                    goto LAB_08021a84;
                  }
                }
LAB_08021be2:
                *puVar1 = uVar12;
              }
            }
LAB_08021a1c:
            iVar9 = iVar9 + 0x9f0;
            puVar16 = puVar1;
            if (puVar24 == puVar1) {
              return local_34;
            }
          } while( true );
        }
        if (ppcVar22 == (code **)&UNK_00000001) goto LAB_08021970;
        if (ppcVar22 == (code **)&UNK_00000012) {
LAB_08021bd0:
          *piVar23 = 2;
          return (code **)&UNK_00000012;
        }
      }
      else {
        ppcVar22 = (code **)&UNK_00000006;
      }
      *piVar23 = 0;
    }
    else {
      ppcVar6 = (code **)FUN_0801e104(DAT_08011484,(int)&local_2c + 2);
      piVar23 = DAT_080219ec;
      if (ppcVar6 == (code **)0x0) {
        FUN_080569f8(DAT_080219f4,DAT_080219f0,uVar19 + 1);
        if (*piVar23 == 3) {
          ppcVar6 = (code **)&UNK_00000001;
        }
        else {
          ppcVar6 = (code **)FUN_080216f8(DAT_080219f4,iVar9);
          if (ppcVar6 == (code **)0x0) goto LAB_080218e2;
        }
        goto LAB_0802193e;
      }
      if (ppcVar6 != (code **)&UNK_00000001) {
        piVar23 = DAT_08021bf4;
        if (ppcVar6 != (code **)&UNK_00000012) {
          *DAT_080219ec = 0;
          return ppcVar6;
        }
        goto LAB_08021bd0;
      }
LAB_08021970:
      ppcVar22 = (code **)&UNK_00000001;
      *piVar23 = 3;
    }
    return ppcVar22;
  case 3:
    iVar9 = FUN_080119b8();
    pcVar10 = DAT_080334c0;
    bVar11 = *(byte *)(iVar9 + 0x92d) + 1;
    bVar20 = bVar11 & 1;
    if (**(code ***)(iVar9 + 0x918) == DAT_080334c0) {
      if ((*(byte *)(iVar9 + 0x92d) != bVar20) &&
         (*(byte *)(iVar9 + 0x92d) = bVar20, *(int *)(iVar9 + 0x924) != 0)) {
        local_24 = CONCAT13(bVar11,(undefined3)local_24) & 0x1ffffff;
        (**(code **)(iVar9 + 0x928))(iVar9 + 0x91c,(int)&local_24 + 3);
      }
    }
    else {
      (***(code ***)(iVar9 + 0x918))(iVar9 + 0x918,bVar20);
    }
    puVar7 = (undefined4 *)FUN_080119b8();
    pcVar17 = DAT_080334c4;
    if (*(code **)*puVar7 == DAT_080334c4) {
      if ((*(char *)(puVar7 + 5) != '\x01') && (*(undefined *)(puVar7 + 5) = 1, puVar7[3] != 0)) {
        local_24 = CONCAT13(1,(undefined3)local_24);
        (*(code *)puVar7[4])(puVar7 + 1,(int)&local_24 + 3);
      }
    }
    else {
      (**(code **)*puVar7)(puVar7,1);
    }
    ppcVar6 = (code **)FUN_0802c818(0xd);
    if (ppcVar6 != (code **)0x0) {
      iVar9 = FUN_080119b8();
      cVar15 = *(char *)(iVar9 + 0x92d);
      iVar9 = 0;
      if (cVar15 != '\0') {
        cVar15 = '\x01';
      }
      do {
        iVar8 = FUN_080119dc(iVar9);
        if (**(code ***)(iVar8 + 0x918) == pcVar10) {
          if ((*(char *)(iVar8 + 0x92d) != cVar15) &&
             (*(char *)(iVar8 + 0x92d) = cVar15, *(int *)(iVar8 + 0x924) != 0)) {
            local_24 = CONCAT13(cVar15,(undefined3)local_24);
            (**(code **)(iVar8 + 0x928))(iVar8 + 0x91c,(int)&local_24 + 3);
          }
        }
        else {
          (***(code ***)(iVar8 + 0x918))(iVar8 + 0x918,cVar15);
        }
        puVar7 = (undefined4 *)FUN_080119dc(iVar9);
        if (*(code **)*puVar7 == pcVar17) {
          if ((*(char *)(puVar7 + 5) != '\x01') && (*(undefined *)(puVar7 + 5) = 1, puVar7[3] != 0))
          {
            local_24 = CONCAT13(1,(undefined3)local_24);
            (*(code *)puVar7[4])(puVar7 + 1,(int)&local_24 + 3);
          }
        }
        else {
          (**(code **)*puVar7)(puVar7,1);
        }
        iVar21 = iVar9 + 1;
        iVar8 = FUN_080119dc(iVar21);
        if (**(code ***)(iVar8 + 0x918) == pcVar10) {
          if ((*(char *)(iVar8 + 0x92d) != cVar15) &&
             (*(char *)(iVar8 + 0x92d) = cVar15, *(int *)(iVar8 + 0x924) != 0)) {
            local_24 = CONCAT13(cVar15,(undefined3)local_24);
            (**(code **)(iVar8 + 0x928))(iVar8 + 0x91c,(int)&local_24 + 3);
          }
        }
        else {
          (***(code ***)(iVar8 + 0x918))(iVar8 + 0x918,cVar15);
        }
        puVar7 = (undefined4 *)FUN_080119dc(iVar21);
        if (*(code **)*puVar7 == pcVar17) {
          ppcVar6 = (code **)(uint)*(byte *)(puVar7 + 5);
          if ((ppcVar6 != (code **)&UNK_00000001) &&
             (*(undefined *)(puVar7 + 5) = 1, puVar7[3] != 0)) {
            local_24 = CONCAT13(1,(undefined3)local_24);
            ppcVar6 = (code **)(*(code *)puVar7[4])(puVar7 + 1,(int)&local_24 + 3);
          }
        }
        else {
          ppcVar6 = (code **)(**(code **)*puVar7)(puVar7,1);
        }
        iVar9 = iVar9 + 2;
      } while (iVar21 != 7);
    }
    break;
  case 0xc:
    iVar9 = FUN_0802c818(0xd);
    if (iVar9 == 0) {
      FUN_08010c48();
      ppcVar6 = (code **)FUN_0803bbf0();
      return ppcVar6;
    }
    iVar9 = FUN_0801134c();
    ppcVar6 = (code **)(uint)(byte)(&DAT_00005055)[iVar9];
    ppcVar22 = (code **)((uint)((int)ppcVar6 + 1) & 1);
    if (**(code ***)(&DAT_00005040 + iVar9) != DAT_080334c8) {
                    /* WARNING: Could not recover jumptable at 0x08033554. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      ppcVar6 = (code **)(***(code ***)(&DAT_00005040 + iVar9))(&DAT_00005040 + iVar9,ppcVar22);
      return ppcVar6;
    }
    if (ppcVar6 != ppcVar22) {
      (&DAT_00005055)[iVar9] = (char)ppcVar22;
      if (*(int *)(&DAT_0000504c + iVar9) != 0) {
        local_24 = CONCAT13((char)ppcVar22,(undefined3)local_24);
        ppcVar6 = (code **)(**(code **)(&DAT_00005050 + iVar9))
                                     (&UNK_00005044 + iVar9,(int)&local_24 + 3);
      }
    }
    break;
  case 0xd:
    ppcVar6 = (code **)FUN_080128a4();
    *DAT_080334bc = (char)ppcVar6;
  }
  return ppcVar6;
}


```