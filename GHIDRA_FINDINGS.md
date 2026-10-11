# Multigrain firmware - SD / file / sound functions (auto-located)

Found by anchor strings, decompiled with immediate callees. Firmware
1.4.8.0, STM32H753, base 0x08000000. For wiring SWD function-calls.

---
## `FUN_0801e104`  @ `0801e104`
- **Anchors:** .wav, /Multigrain/Wavs, SD: Collect Sound
- **Strings seen:** %s-%d.wav | /Multigrain/Wavs | SD: Collect Sound %d: 
- **Signature:** `undefined FUN_0801e104()`
- **Params:** 0  **Calls:** 17 funcs

```c

/* WARNING: Removing unreachable block (ram,0x0801e774) */

char FUN_0801e104(int param_1,char *param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  char cVar3;
  int iVar4;
  undefined4 uVar5;
  code *pcVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int local_65c;
  char local_649;
  uint local_648;
  uint uStack_644;
  undefined auStack_640 [256];
  undefined auStack_540 [256];
  undefined auStack_440 [256];
  int local_340 [64];
  uint local_240 [64];
  int local_140 [71];
  
  uVar1 = DAT_0801e37c;
  iVar7 = 0;
  *DAT_0801e378 = 1;
  local_649 = '\0';
  FUN_0804cb58(uVar1);
  FUN_08051058(DAT_0801e384,DAT_0801e380,1);
  local_65c = param_1 + 0x7dc;
  *param_2 = '\0';
  uVar1 = DAT_0801e388;
  param_1 = param_1 + 0x58c;
  do {
    iVar7 = iVar7 + 1;
    FUN_0804cb68(DAT_0801e38c,iVar7);
    FUN_08056428(auStack_640,0,0x100);
    cVar3 = *(char *)(param_1 + 0x10);
    if (cVar3 != '\x01') {
      if (cVar3 == '\x02') {
        if (*(char *)(param_1 + 0x28) == '\0') goto LAB_0801e4d6;
        local_649 = FUN_08051eb0(DAT_0801e6dc);
        if (local_649 != '\0') goto LAB_0801e702;
        FUN_08007160(auStack_640,param_1 + 0x28,0x100);
        FUN_0804cb68(DAT_0801e6e0,DAT_0801e6dc,auStack_640);
      }
      else if (cVar3 == '\0') {
        if (*(char *)(param_1 + 0x250) == '\0') goto LAB_0801e4d6;
        FUN_0804cb68(DAT_0801e6e8,local_65c);
        goto LAB_0801e48a;
      }
LAB_0801e166:
      local_649 = FUN_080510f0(uVar1,auStack_640,1);
      if (local_649 == '\0') {
        cVar3 = FUN_08051eb0(DAT_0801e390);
        if (cVar3 != '\0') {
          FUN_08051d88(DAT_0801e7a0);
          if (cVar3 != '\x01') {
            if (cVar3 != '\x12') {
              *DAT_0801e7a4 = 0;
              return cVar3;
            }
            goto LAB_0801e56a;
          }
          goto LAB_0801e70c;
        }
        local_649 = FUN_0805241c(auStack_640,local_140);
        if ((local_649 != '\0') && (iVar4 = DAT_0801e7a0, local_649 != '\x04')) {
LAB_0801e6fe:
          FUN_08051d88(iVar4);
          goto LAB_0801e702;
        }
        FUN_08007160(auStack_540,auStack_640,0x100);
        iVar4 = DAT_0801e394;
        if (local_649 == '\x04') {
          FUN_08007160(auStack_540,auStack_640,0x100);
LAB_0801e338:
          FUN_0804cb68(DAT_0801e39c,auStack_540);
          local_649 = FUN_080510f0(DAT_0801e3a0,auStack_540,10);
          uVar5 = DAT_0801e3a0;
          if (local_649 == '\0') {
            FUN_08051f1c(uVar1);
            uVar2 = DAT_0801e3ac;
            FUN_08051f1c(uVar5,0);
            do {
              local_649 = FUN_080513f8(uVar1,uVar2,0x1000,&local_648);
              if (local_648 == 0) break;
              local_649 = FUN_08051884(uVar5,uVar2,local_648,&uStack_644);
            } while (local_648 <= uStack_644);
            FUN_08051d88(uVar1);
            FUN_08051d88(DAT_0801e6c0);
            if (**(code ***)(param_1 + -4) == DAT_0801e6c4) {
              if ((*(char *)(param_1 + 0x10) != '\0') &&
                 (*(undefined *)(param_1 + 0x10) = 0, *(int *)(param_1 + 8) != 0)) {
                local_240[0] = local_240[0] & 0xffffff00;
                (**(code **)(param_1 + 0xc))(param_1,local_240);
              }
            }
            else {
              (***(code ***)(param_1 + -4))(param_1 + -4,0);
            }
            FUN_08007160(local_340,auStack_540,0x100);
            pcVar6 = **(code ***)(param_1 + 0x23c);
            FUN_08007160(auStack_440,local_340,0x100);
            if (pcVar6 == DAT_0801e6c8) {
              iVar4 = FUN_08056a38(auStack_440,local_65c,0x100);
              if ((iVar4 != 0) &&
                 (uVar5 = FUN_08007160(param_1 + 0x250,auStack_440,0x100),
                 *(int *)(param_1 + 0x248) != 0)) {
                FUN_08007160(local_240,uVar5,0x100);
                (**(code **)(param_1 + 0x24c))(param_1 + 0x240,local_240);
              }
            }
            else {
              (*pcVar6)(param_1 + 0x23c,auStack_440);
            }
            uVar5 = DAT_0801e6cc;
            *param_2 = '\x01';
            FUN_0804cb58(uVar5);
            goto LAB_0801e48a;
          }
        }
        else {
          FUN_0804cb58(DAT_0801e398);
          if (*(int *)(iVar4 + 0x248) == local_140[0]) {
            local_649 = FUN_080510f0(iVar4 + 0x46c,auStack_640,1);
            if (local_649 != '\0') {
              iVar4 = iVar4 + 0x23c;
              goto LAB_0801e6fe;
            }
            FUN_08051f1c(uVar1);
            uVar2 = DAT_0801e6f8;
            uVar5 = DAT_0801e6f4;
            FUN_08051f1c(iVar4 + 0x46c,0);
            do {
              local_649 = FUN_080513f8(uVar1,uVar5,0x1000,local_340);
              if ((local_340[0] == 0) ||
                 (local_649 = FUN_080513f8(DAT_0801e6c0,uVar2,local_340[0],local_240),
                 local_240[0] == 0)) {
                if (local_649 != '\0') goto LAB_0801e702;
                FUN_0804cb58(DAT_0801e6f0);
                FUN_08051d88(uVar1);
                FUN_08051d88(DAT_0801e6c0);
                if (**(code ***)(param_1 + -4) == DAT_0801e6c4) {
                  if ((*(char *)(param_1 + 0x10) != '\0') &&
                     (*(undefined *)(param_1 + 0x10) = 0, *(int *)(param_1 + 8) != 0)) {
                    local_240[0] = local_240[0] & 0xffffff00;
                    (**(code **)(param_1 + 0xc))(param_1,local_240);
                  }
                }
                else {
                  (***(code ***)(param_1 + -4))(param_1 + -4,0);
                }
                FUN_08007160(local_340,auStack_540,0x100);
                pcVar6 = **(code ***)(param_1 + 0x23c);
                FUN_08007160(auStack_440,local_340,0x100);
                if (pcVar6 == DAT_0801e6c8) {
                  iVar4 = FUN_08056a38(auStack_440,local_65c,0x100);
                  if ((iVar4 != 0) &&
                     (uVar5 = FUN_08007160(param_1 + 0x250,auStack_440,0x100),
                     *(int *)(param_1 + 0x248) != 0)) {
                    FUN_08007160(local_240,uVar5,0x100);
                    (**(code **)(param_1 + 0x24c))(param_1 + 0x240,local_240);
                  }
                }
                else {
                  (*pcVar6)(param_1 + 0x23c,auStack_440);
                }
                *param_2 = '\x01';
                goto LAB_0801e48a;
              }
              if (local_649 != '\0') {
                if (local_649 != '\x01') goto LAB_0801e4b8;
                goto LAB_0801e70c;
              }
              iVar4 = FUN_080562cc(uVar5,uVar2,local_340[0]);
            } while (iVar4 == 0);
            FUN_0804cb58(DAT_0801e7ac);
            FUN_08051d88(DAT_0801e7b0);
          }
          uVar5 = DAT_0801e3a4;
          iVar4 = FUN_08007580(auStack_640);
          uVar2 = DAT_0801e3a8;
          auStack_640[iVar4 + -4] = 0;
          FUN_080569f8(auStack_540,uVar5,auStack_640,1);
          FUN_0804cb68(uVar2,auStack_540);
          local_649 = FUN_0805241c(auStack_540,local_140);
          if (local_649 == '\x04') goto LAB_0801e338;
          if (local_649 == '\0') {
            FUN_080569f8(auStack_540,uVar5,auStack_640,2);
            iVar4 = 3;
            FUN_0804cb68(uVar2,auStack_540);
            local_649 = FUN_0805241c(auStack_540,local_140);
            if (local_649 != '\x04') {
              if (local_649 != '\0') goto LAB_0801e554;
              while( true ) {
                FUN_080569f8(auStack_540,uVar5,auStack_640,iVar4);
                iVar9 = iVar4 + 1;
                FUN_0804cb68(uVar2,auStack_540);
                iVar8 = iVar4 + 2;
                local_649 = FUN_0805241c(auStack_540,local_140);
                iVar4 = iVar4 + 3;
                if (local_649 == '\x04') break;
                if (local_649 != '\0') goto LAB_0801e554;
                FUN_080569f8(auStack_540,uVar5,auStack_640,iVar9);
                FUN_0804cb68(uVar2,auStack_540);
                local_649 = FUN_0805241c(auStack_540,local_140);
                if (local_649 == '\x04') break;
                if (local_649 != '\0') goto LAB_0801e554;
                FUN_080569f8(auStack_540,uVar5,auStack_640,iVar8);
                FUN_0804cb68(uVar2,auStack_540);
                local_649 = FUN_0805241c(auStack_540,local_140);
                if (local_649 == '\x04') break;
                if (local_649 != '\0') goto LAB_0801e554;
                if (iVar4 == 99) {
                  FUN_08051d88(DAT_0801e388);
                  *DAT_0801e378 = 2;
                  return '\x12';
                }
              }
            }
            goto LAB_0801e338;
          }
        }
LAB_0801e554:
        FUN_08051d88(DAT_0801e6ec);
      }
      if (local_649 == '\x01') {
LAB_0801e70c:
        *DAT_0801e7a4 = 3;
        return '\x01';
      }
      if (local_649 == '\x12') {
LAB_0801e56a:
        *DAT_0801e6d4 = 2;
        return '\x12';
      }
      goto LAB_0801e4be;
    }
    if (*(char *)(param_1 + 0x13c) != '\0') {
      local_649 = FUN_08051eb0(DAT_0801e6e4);
      if (local_649 == '\0') {
        FUN_08007160(auStack_640,param_1 + 0x13c,0x100);
        FUN_0804cb68(DAT_0801e6e0,DAT_0801e6e4,auStack_640);
        goto LAB_0801e166;
      }
LAB_0801e702:
      if (local_649 != '\x01') {
        FUN_0801d860(local_649);
        return local_649;
      }
      goto LAB_0801e70c;
    }
LAB_0801e4d6:
    FUN_0804cb58(DAT_0801e6d8);
LAB_0801e48a:
    param_1 = param_1 + 0x9f0;
    local_65c = local_65c + 0x9f0;
  } while (iVar7 != 8);
  if (*param_2 != '\0') {
    FUN_0804cb58(DAT_0801e7a8);
  }
  FUN_0804cb58(DAT_0801e6d0);
  if (local_649 == '\x01') {
    *DAT_0801e7a4 = 3;
    return '\x01';
  }
LAB_0801e4b8:
  if (local_649 == '\x12') {
    *DAT_0801e6d4 = 2;
  }
  else {
LAB_0801e4be:
    *DAT_0801e6d4 = 0;
  }
  return local_649;
}


```

### callee `FUN_0804cb58` @ `0804cb58`
```c

uint FUN_0804cb58(int param_1)

{
  bool bVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined4 uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  int iVar12;
  
  puVar3 = DAT_0805329c;
  uVar4 = FUN_08007580(param_1);
  uVar8 = DAT_08053290;
  puVar2 = DAT_0805328c;
  if (*(char *)puVar3 == '\0') {
    *(undefined4 *)((int)puVar3 + 7) = *DAT_08053288;
    puVar3[10] = 0;
    uVar6 = DAT_08053294;
    puVar3[9] = 0;
    puVar3[0xb] = 0;
    puVar3[0x1c] = 0;
    puVar3[0x1b] = 0;
    puVar3[0x1d] = 0;
    puVar3[6] = uVar8;
    puVar3[0x18] = uVar8;
    *(char *)((int)puVar3 + 6) = ' ';
    puVar3[7] = uVar6;
    puVar3[8] = 0x400;
    uVar8 = *puVar2;
    uVar6 = puVar2[1];
    puVar3[4] = 3;
    puVar3[5] = 3;
    *puVar3 = uVar8;
    *(short *)(puVar3 + 1) = (short)uVar6;
    uVar8 = DAT_08053298;
    puVar3[0x1a] = 0x10;
    puVar3[0x19] = uVar8;
  }
  uVar8 = 0;
  bVar1 = (bool)isCurrentModePrivileged();
  if (bVar1) {
    uVar8 = getBasePriority();
  }
  bVar1 = (bool)isCurrentModePrivileged();
  if (bVar1) {
    setBasePriority(0x20);
  }
  iVar12 = puVar3[0xb];
  if (iVar12 != 1) {
    if (iVar12 == 2) {
      uVar11 = puVar3[9];
      uVar7 = 0;
LAB_0805315e:
      uVar9 = puVar3[10];
      if (uVar9 <= uVar11) goto LAB_080531b2;
      do {
        uVar9 = (uVar9 - 1) - uVar11;
        iVar12 = puVar3[8];
        while( true ) {
          if (uVar4 <= uVar9) {
            uVar9 = uVar4;
          }
          iVar5 = puVar3[7] + uVar11;
          uVar10 = iVar12 - uVar11;
          if (uVar9 <= iVar12 - uVar11) {
            uVar10 = uVar9;
          }
          uVar11 = uVar11 + uVar10;
          FUN_08007160(iVar5,param_1,uVar10,puVar3 + 6,uVar8);
          uVar4 = uVar4 - uVar10;
          uVar7 = uVar7 + uVar10;
          param_1 = param_1 + uVar10;
          if (uVar11 == puVar3[8]) {
            uVar11 = 0;
            puVar3[9] = 0;
            if (uVar4 == 0) goto LAB_0805309a;
            goto LAB_0805315e;
          }
          puVar3[9] = uVar11;
          if (uVar4 == 0) goto LAB_0805309a;
          uVar9 = puVar3[10];
          if (uVar11 < uVar9) break;
LAB_080531b2:
          iVar12 = puVar3[8];
          uVar9 = (uVar9 + iVar12 + -1) - uVar11;
        }
      } while( true );
    }
    if (iVar12 == 0) {
      uVar7 = puVar3[10];
      uVar11 = puVar3[9];
      if (uVar7 <= uVar11) {
        uVar7 = uVar7 + puVar3[8];
      }
      uVar9 = (uVar7 - 1) - uVar11;
      uVar7 = 0;
      if (uVar4 <= uVar9) {
        iVar12 = puVar3[8];
        uVar7 = iVar12 - uVar11;
        if (uVar4 < uVar7) {
          FUN_08007160(puVar3[7] + uVar11,param_1,uVar4,uVar9,uVar8);
          puVar3[9] = uVar11 + uVar4;
          uVar7 = uVar4;
        }
        else {
          FUN_08007160(puVar3[7] + uVar11,param_1,uVar7,uVar9,uVar8);
          iVar12 = (uVar11 - iVar12) + uVar4;
          FUN_08007160(puVar3[7],param_1 + uVar7,iVar12);
          puVar3[9] = iVar12;
          uVar7 = uVar4;
        }
      }
    }
    else {
      uVar7 = 0;
    }
    goto LAB_0805309a;
  }
  uVar7 = puVar3[10];
  uVar11 = puVar3[9];
  if (uVar11 < uVar7) {
    iVar12 = puVar3[8];
    uVar7 = (uVar7 - 1) - uVar11;
    uVar9 = iVar12 - uVar11;
    if (uVar4 <= uVar7) {
      uVar7 = uVar4;
    }
    if (uVar9 <= uVar7) {
LAB_0805321e:
      FUN_08007160(puVar3[7] + uVar11,param_1,uVar9,uVar8,uVar8);
      iVar12 = uVar11 + (uVar7 - iVar12);
      FUN_08007160(puVar3[7],param_1 + uVar9,iVar12);
      puVar3[9] = iVar12;
      goto LAB_0805309a;
    }
  }
  else {
    iVar12 = puVar3[8];
    uVar9 = iVar12 - uVar11;
    uVar7 = (uVar7 + iVar12 + -1) - uVar11;
    if (uVar4 <= uVar7) {
      uVar7 = uVar4;
    }
    if (uVar9 <= uVar7) goto LAB_0805321e;
  }
  FUN_08007160(puVar3[7] + uVar11,param_1,uVar7,uVar8,uVar8);
  puVar3[9] = uVar11 + uVar7;
LAB_0805309a:
  bVar1 = (bool)isCurrentModePrivileged();
  if (bVar1) {
    setBasePriority(uVar8);
  }
  return uVar7;
}


```

### callee `FUN_080562cc` @ `080562cc`
```c

int FUN_080562cc(int *param_1,int *param_2,uint param_3)

{
  int *piVar1;
  int *piVar2;
  byte *pbVar3;
  byte *pbVar4;
  
  if (3 < param_3) {
    piVar1 = param_1;
    piVar2 = param_2;
    if ((((uint)param_1 | (uint)param_2) & 3) != 0) goto LAB_08056302;
    do {
      param_1 = piVar1 + 1;
      param_2 = piVar2 + 1;
      if (*piVar1 != *piVar2) goto LAB_08056302;
      param_3 = param_3 - 4;
      piVar2 = param_2;
      piVar1 = param_1;
    } while (3 < param_3);
  }
  piVar1 = param_1;
  piVar2 = param_2;
  if (param_3 == 0) {
    return 0;
  }
LAB_08056302:
  pbVar4 = (byte *)((int)piVar1 - 1);
  pbVar3 = (byte *)((int)piVar2 - 1);
  do {
    pbVar4 = pbVar4 + 1;
    pbVar3 = pbVar3 + 1;
    if ((uint)*pbVar4 != (uint)*pbVar3) {
      return (uint)*pbVar4 - (uint)*pbVar3;
    }
  } while ((int)piVar1 + ((param_3 - 1) - (int)pbVar4) != 0);
  return 0;
}


```

### callee `FUN_08051884` @ `08051884`
```c

char FUN_08051884(char **param_1,undefined4 *param_2,uint param_3,int *param_4)

{
  byte bVar1;
  char *pcVar2;
  int iVar3;
  char **ppcVar4;
  undefined4 *puVar5;
  uint *puVar6;
  uint uVar7;
  undefined4 *puVar8;
  char *pcVar9;
  char **ppcVar10;
  char **ppcVar11;
  uint uVar12;
  undefined4 *puVar13;
  char **ppcVar14;
  char **ppcVar15;
  undefined *puVar16;
  undefined4 *puVar17;
  char **ppcVar18;
  undefined4 *puVar19;
  char *pcVar20;
  char cVar21;
  uint uVar22;
  
  *param_4 = 0;
  if ((((param_1 == (char **)0x0) || (pcVar2 = *param_1, pcVar2 == (char *)0x0)) ||
      (*pcVar2 == '\0')) ||
     ((*(short *)(param_1 + 1) != *(short *)(pcVar2 + 6) ||
      (iVar3 = FUN_08052c2c(pcVar2[1]), iVar3 << 0x1f < 0)))) {
    cVar21 = '\t';
  }
  else {
    cVar21 = *(char *)((int)param_1 + 0x15);
    if (cVar21 == '\0') {
      bVar1 = *(byte *)(param_1 + 5);
      if ((int)((uint)bVar1 << 0x1e) < 0) {
        pcVar2 = param_1[6];
        if (CARRY4((uint)pcVar2,param_3) != false) {
          param_3 = ~(uint)pcVar2;
        }
        if (param_3 != 0) {
          ppcVar4 = param_1 + 0x8c;
          ppcVar18 = param_1 + 0xc;
          pcVar20 = *param_1;
          do {
            uVar7 = (uint)pcVar2 & 0x1ff;
            if (uVar7 == 0) {
              uVar7 = *(ushort *)(pcVar20 + 10) - 1 & (uint)pcVar2 >> 9;
              if (uVar7 == 0) {
                if (pcVar2 == (char *)0x0) {
                  pcVar2 = param_1[2];
                  if (pcVar2 == (char *)0x0) {
                    pcVar2 = (char *)FUN_0804f088(param_1,0);
                    goto joined_r0x08051b38;
                  }
                }
                else {
                  if (param_1[0xb] == (char *)0x0) {
                    pcVar2 = (char *)FUN_0804f088(param_1,param_1[7]);
                  }
                  else {
                    puVar6 = (uint *)(param_1[0xb] + 4);
                    uVar12 = ((uint)pcVar2 >> 9) / (uint)*(ushort *)(*param_1 + 10);
                    uVar22 = *puVar6;
                    while( true ) {
                      if (uVar22 == 0) goto LAB_080519b2;
                      if (uVar12 < uVar22) break;
                      uVar12 = uVar12 - uVar22;
                      puVar6 = puVar6 + 2;
                      uVar22 = *puVar6;
                    }
                    pcVar2 = (char *)(puVar6[1] + uVar12);
                  }
joined_r0x08051b38:
                  if (pcVar2 == (char *)0x0) break;
                }
                if (pcVar2 == &UNK_00000001) goto LAB_08051afc;
                if (pcVar2 == (char *)0xffffffff) goto LAB_08051b5a;
                param_1[7] = pcVar2;
                if (param_1[2] == (char *)0x0) {
                  param_1[2] = pcVar2;
                }
              }
              if (*(char *)(param_1 + 5) < '\0') {
                iVar3 = FUN_08052c80(pcVar20[1],ppcVar18,param_1[8],1);
                if (iVar3 != 0) goto LAB_08051b5a;
                *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0x7f;
              }
              if ((char *)(*(int *)(pcVar20 + 0x1c) + -2) <= param_1[7] + -2) {
LAB_08051afc:
                *(undefined *)((int)param_1 + 0x15) = 2;
                return '\x02';
              }
              uVar12 = (uint)*(ushort *)(pcVar20 + 10);
              iVar3 = uVar12 * (int)(param_1[7] + -2) + *(int *)(pcVar20 + 0x30);
              if (iVar3 == 0) goto LAB_08051afc;
              pcVar2 = (char *)(uVar7 + iVar3);
              if (param_3 < 0x200) {
                pcVar9 = param_1[6];
                if ((param_1[8] != pcVar2) && (pcVar9 < param_1[3])) {
                  iVar3 = FUN_08052c64(pcVar20[1],ppcVar18,pcVar2,1);
                  if (iVar3 != 0) goto LAB_08051b5a;
                  pcVar9 = param_1[6];
                }
                uVar7 = (uint)pcVar9 & 0x1ff;
                param_1[8] = pcVar2;
                goto LAB_080519d8;
              }
              uVar22 = param_3 >> 9;
              if (uVar12 < uVar7 + (param_3 >> 9)) {
                uVar22 = uVar12 - uVar7;
              }
              iVar3 = FUN_08052c80(pcVar20[1],param_2,pcVar2,uVar22);
              if (iVar3 != 0) {
LAB_08051b5a:
                *(undefined *)((int)param_1 + 0x15) = 1;
                return '\x01';
              }
              if ((uint)((int)param_1[8] - (int)pcVar2) < uVar22) {
                ppcVar11 = (char **)(param_2 + ((int)param_1[8] - (int)pcVar2) * 0x80);
                if ((uint)((int)ppcVar18 - ((int)ppcVar11 + 1)) < 3) {
                  puVar16 = (undefined *)((int)param_1 + 0x2f);
                  ppcVar10 = ppcVar11;
                  do {
                    ppcVar15 = ppcVar10 + 2;
                    puVar16[1] = *(undefined *)ppcVar10;
                    puVar16[2] = *(undefined *)((int)ppcVar10 + 1);
                    puVar16[3] = *(undefined *)((int)ppcVar10 + 2);
                    puVar16[4] = *(undefined *)((int)ppcVar10 + 3);
                    puVar16[5] = *(undefined *)(ppcVar10 + 1);
                    puVar16[6] = *(undefined *)((int)ppcVar10 + 5);
                    puVar16[7] = *(undefined *)((int)ppcVar10 + 6);
                    puVar16 = puVar16 + 8;
                    *puVar16 = *(undefined *)((int)ppcVar10 + 7);
                    ppcVar10 = ppcVar15;
                  } while (ppcVar11 + 0x80 != ppcVar15);
                }
                else {
                  uVar7 = ((uint)((int)ppcVar4 + (-4 - (int)ppcVar18)) >> 2) + 1 & 7;
                  ppcVar10 = ppcVar18;
                  if (uVar7 != 0) {
                    ppcVar15 = ppcVar18;
                    if (uVar7 != 1) {
                      ppcVar10 = ppcVar11;
                      ppcVar14 = ppcVar18;
                      if (uVar7 != 2) {
                        if (uVar7 != 3) {
                          if (uVar7 != 4) {
                            if (uVar7 != 5) {
                              if (uVar7 != 6) {
                                ppcVar10 = ppcVar11 + 1;
                                ppcVar14 = param_1 + 0xd;
                                *ppcVar18 = *ppcVar11;
                              }
                              ppcVar11 = ppcVar10 + 1;
                              ppcVar15 = ppcVar14 + 1;
                              *ppcVar14 = *ppcVar10;
                            }
                            ppcVar10 = ppcVar11 + 1;
                            ppcVar14 = ppcVar15 + 1;
                            *ppcVar15 = *ppcVar11;
                          }
                          ppcVar11 = ppcVar10 + 1;
                          ppcVar15 = ppcVar14 + 1;
                          *ppcVar14 = *ppcVar10;
                        }
                        ppcVar10 = ppcVar11 + 1;
                        ppcVar14 = ppcVar15 + 1;
                        *ppcVar15 = *ppcVar11;
                      }
                      ppcVar11 = ppcVar10 + 1;
                      ppcVar15 = ppcVar14 + 1;
                      *ppcVar14 = *ppcVar10;
                    }
                    *ppcVar15 = *ppcVar11;
                    ppcVar11 = ppcVar11 + 1;
                    ppcVar10 = ppcVar15 + 1;
                    if (ppcVar15 + 1 == ppcVar4) goto LAB_08051d38;
                  }
                  do {
                    ppcVar15 = ppcVar10 + 8;
                    *ppcVar10 = *ppcVar11;
                    ppcVar10[1] = ppcVar11[1];
                    ppcVar10[2] = ppcVar11[2];
                    ppcVar10[3] = ppcVar11[3];
                    ppcVar10[4] = ppcVar11[4];
                    ppcVar10[5] = ppcVar11[5];
                    ppcVar10[6] = ppcVar11[6];
                    ppcVar10[7] = ppcVar11[7];
                    ppcVar11 = ppcVar11 + 8;
                    ppcVar10 = ppcVar15;
                  } while (ppcVar15 != ppcVar4);
                }
LAB_08051d38:
                *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0x7f;
              }
              puVar5 = param_2 + uVar22 * 0x80;
              uVar22 = uVar22 << 9;
            }
            else {
LAB_080519d8:
              puVar8 = (undefined4 *)(uVar7 + (int)ppcVar18);
              uVar22 = 0x200 - uVar7;
              if (param_3 <= 0x200 - uVar7) {
                uVar22 = param_3;
              }
              uVar7 = uVar22 - 1;
              if (((uint)((int)puVar8 - (int)((int)param_2 + 1)) < 3) || (uVar7 < 8)) {
                puVar5 = (undefined4 *)((int)param_2 + uVar22);
                puVar19 = (undefined4 *)((int)puVar8 + -1);
                uVar7 = (int)puVar5 - (int)param_2 & 7;
                if (uVar7 == 0) goto LAB_08051bde;
                if (uVar7 != 1) {
                  puVar17 = param_2;
                  if (uVar7 != 2) {
                    if (uVar7 != 3) {
                      if (uVar7 != 4) {
                        if (uVar7 != 5) {
                          if (uVar7 != 6) {
                            puVar17 = (undefined4 *)((int)param_2 + 1);
                            *(undefined *)puVar8 = *(undefined *)param_2;
                            puVar19 = puVar8;
                          }
                          param_2 = (undefined4 *)((int)puVar17 + 1);
                          puVar19 = (undefined4 *)((int)puVar19 + 1);
                          *(undefined *)puVar19 = *(undefined *)puVar17;
                        }
                        puVar17 = (undefined4 *)((int)param_2 + 1);
                        puVar19 = (undefined4 *)((int)puVar19 + 1);
                        *(undefined *)puVar19 = *(undefined *)param_2;
                      }
                      param_2 = (undefined4 *)((int)puVar17 + 1);
                      puVar19 = (undefined4 *)((int)puVar19 + 1);
                      *(undefined *)puVar19 = *(undefined *)puVar17;
                    }
                    puVar17 = (undefined4 *)((int)param_2 + 1);
                    puVar19 = (undefined4 *)((int)puVar19 + 1);
                    *(undefined *)puVar19 = *(undefined *)param_2;
                  }
                  param_2 = (undefined4 *)((int)puVar17 + 1);
                  puVar19 = (undefined4 *)((int)puVar19 + 1);
                  *(undefined *)puVar19 = *(undefined *)puVar17;
                }
                puVar19 = (undefined4 *)((int)puVar19 + 1);
                *(undefined *)puVar19 = *(undefined *)param_2;
                for (param_2 = (undefined4 *)((int)param_2 + 1); param_2 != puVar5;
                    param_2 = param_2 + 2) {
LAB_08051bde:
                  *(undefined *)((int)puVar19 + 1) = *(undefined *)param_2;
                  *(undefined *)((int)puVar19 + 2) = *(undefined *)((int)param_2 + 1);
                  *(undefined *)((int)puVar19 + 3) = *(undefined *)((int)param_2 + 2);
                  *(undefined *)(puVar19 + 1) = *(undefined *)((int)param_2 + 3);
                  *(undefined *)((int)puVar19 + 5) = *(undefined *)(param_2 + 1);
                  *(undefined *)((int)puVar19 + 6) = *(undefined *)((int)param_2 + 5);
                  *(undefined *)((int)puVar19 + 7) = *(undefined *)((int)param_2 + 6);
                  puVar19 = puVar19 + 2;
                  *(undefined *)puVar19 = *(undefined *)((int)param_2 + 7);
                }
              }
              else {
                uVar12 = ((uVar22 & 0xfffffffc) - 4 >> 2) + 1 & 7;
                puVar19 = param_2;
                puVar5 = puVar8;
                if (uVar12 == 0) goto LAB_08051aae;
                if (uVar12 != 1) {
                  puVar17 = param_2;
                  puVar13 = puVar8;
                  if (uVar12 != 2) {
                    if (uVar12 != 3) {
                      if (uVar12 != 4) {
                        if (uVar12 != 5) {
                          if (uVar12 != 6) {
                            puVar17 = param_2 + 1;
                            puVar13 = puVar8 + 1;
                            *puVar8 = *param_2;
                          }
                          puVar19 = puVar17 + 1;
                          puVar5 = puVar13 + 1;
                          *puVar13 = *puVar17;
                        }
                        puVar17 = puVar19 + 1;
                        puVar13 = puVar5 + 1;
                        *puVar5 = *puVar19;
                      }
                      puVar19 = puVar17 + 1;
                      puVar5 = puVar13 + 1;
                      *puVar13 = *puVar17;
                    }
                    puVar17 = puVar19 + 1;
                    puVar13 = puVar5 + 1;
                    *puVar5 = *puVar19;
                  }
                  puVar19 = puVar17 + 1;
                  puVar5 = puVar13 + 1;
                  *puVar13 = *puVar17;
                }
                *puVar5 = *puVar19;
                puVar19 = puVar19 + 1;
                for (puVar5 = puVar5 + 1;
                    puVar5 != (undefined4 *)((uVar22 & 0xfffffffc) + (int)puVar8);
                    puVar5 = puVar5 + 8) {
LAB_08051aae:
                  *puVar5 = *puVar19;
                  puVar5[1] = puVar19[1];
                  puVar5[2] = puVar19[2];
                  puVar5[3] = puVar19[3];
                  puVar5[4] = puVar19[4];
                  puVar5[5] = puVar19[5];
                  puVar5[6] = puVar19[6];
                  puVar5[7] = puVar19[7];
                  puVar19 = puVar19 + 8;
                }
                uVar12 = uVar22 & 0xfffffffc;
                puVar5 = (undefined4 *)((int)param_2 + uVar12);
                if (uVar22 != uVar12) {
                  *(undefined *)((int)puVar8 + uVar12) = *(undefined *)((int)param_2 + uVar12);
                  if ((uVar7 != uVar12) &&
                     (*(undefined *)((int)puVar8 + uVar12 + 1) = *(undefined *)((int)puVar5 + 1),
                     uVar7 - uVar12 != 1)) {
                    *(undefined *)((int)puVar8 + uVar12 + 2) = *(undefined *)((int)puVar5 + 2);
                  }
                  puVar5 = (undefined4 *)((int)param_2 + uVar22);
                }
              }
              *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) | 0x80;
            }
            pcVar2 = param_1[6] + uVar22;
            iVar3 = *param_4;
            param_1[6] = pcVar2;
            pcVar9 = param_1[3];
            if (param_1[3] < pcVar2) {
              pcVar9 = pcVar2;
            }
            param_3 = param_3 - uVar22;
            param_1[3] = pcVar9;
            *param_4 = iVar3 + uVar22;
            param_2 = puVar5;
          } while (param_3 != 0);
LAB_080519b2:
          bVar1 = *(byte *)(param_1 + 5);
        }
        *(byte *)(param_1 + 5) = bVar1 | 0x40;
      }
      else {
        cVar21 = '\a';
      }
    }
  }
  return cVar21;
}


```

### callee `FUN_08007160` @ `08007160`
```c

undefined4 * FUN_08007160(undefined4 *param_1,undefined4 *param_2,uint param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  uint uVar4;
  uint uVar5;
  bool bVar6;
  
  puVar2 = param_1;
  if ((((uint)param_2 | (uint)param_1) & 3) != 0) {
    if (param_3 < 8) {
      uVar5 = param_3 - 4;
      if (3 < param_3) {
        do {
          puVar1 = param_2;
          puVar3 = puVar2;
          bVar6 = uVar5 != 0;
          uVar5 = uVar5 - 1;
          *(undefined *)puVar3 = *(undefined *)puVar1;
          puVar2 = (undefined4 *)((int)puVar3 + 1);
          param_2 = (undefined4 *)((int)puVar1 + 1);
        } while (bVar6);
        *(undefined *)(undefined4 *)((int)puVar3 + 1) =
             *(undefined *)(undefined4 *)((int)puVar1 + 1);
        *(undefined *)((int)puVar3 + 2) = *(undefined *)((int)puVar1 + 2);
        *(undefined *)((int)puVar3 + 3) = *(undefined *)((int)puVar1 + 3);
        return param_1;
      }
      goto LAB_0800722c;
    }
    if ((((uint)param_2 & 3) != 0) && (((uint)param_1 & 3) != 0)) {
      uVar5 = 4 - ((uint)param_1 & 3);
      param_3 = param_3 - uVar5;
      puVar1 = param_1;
      puVar3 = param_2;
      if (((uint)param_1 & 1) != 0) {
        puVar3 = (undefined4 *)((int)param_2 + 1);
        puVar1 = (undefined4 *)((int)param_1 + 1);
        *(undefined *)param_1 = *(undefined *)param_2;
      }
      puVar2 = puVar1;
      param_2 = puVar3;
      if ((uVar5 & 2) != 0) {
        param_2 = (undefined4 *)((int)puVar3 + 2);
        puVar2 = (undefined4 *)((int)puVar1 + 2);
        *(undefined2 *)puVar1 = *(undefined2 *)puVar3;
      }
    }
  }
  while (0x3f < param_3) {
    *puVar2 = *param_2;
    puVar2[1] = param_2[1];
    puVar2[2] = param_2[2];
    puVar2[3] = param_2[3];
    puVar2[4] = param_2[4];
    puVar2[5] = param_2[5];
    puVar2[6] = param_2[6];
    puVar2[7] = param_2[7];
    puVar2[8] = param_2[8];
    puVar2[9] = param_2[9];
    puVar2[10] = param_2[10];
    puVar2[0xb] = param_2[0xb];
    puVar2[0xc] = param_2[0xc];
    puVar2[0xd] = param_2[0xd];
    puVar2[0xe] = param_2[0xe];
    puVar2[0xf] = param_2[0xf];
    puVar2 = puVar2 + 0x10;
    param_2 = param_2 + 0x10;
    param_3 = param_3 - 0x40;
  }
  uVar4 = param_3 - 0x10;
  if (0xffffffcf < param_3 - 0x40) {
    do {
      *puVar2 = *param_2;
      puVar2[1] = param_2[1];
      puVar1 = param_2 + 3;
      puVar3 = puVar2 + 3;
      puVar2[2] = param_2[2];
      param_2 = param_2 + 4;
      puVar2 = puVar2 + 4;
      *puVar3 = *puVar1;
      bVar6 = 0xf < uVar4;
      uVar4 = uVar4 - 0x10;
    } while (bVar6);
  }
  uVar5 = uVar4 + 0xc;
  puVar3 = puVar2;
  puVar1 = param_2;
  if (0xfffffff3 < uVar4) {
    do {
      param_2 = puVar1 + 1;
      *puVar3 = *puVar1;
      bVar6 = 3 < uVar5;
      uVar5 = uVar5 - 4;
      puVar2 = puVar3 + 1;
      puVar3 = puVar3 + 1;
      puVar1 = param_2;
    } while (bVar6);
  }
LAB_0800722c:
  if (uVar5 + 4 != 0) {
    puVar1 = puVar2;
    puVar3 = param_2;
    if ((uVar5 & 1) != 0) {
      puVar3 = (undefined4 *)((int)param_2 + 1);
      puVar1 = (undefined4 *)((int)puVar2 + 1);
      *(undefined *)puVar2 = *(undefined *)param_2;
    }
    if ((uVar5 + 4 & 2) != 0) {
      *(undefined2 *)puVar1 = *(undefined2 *)puVar3;
    }
  }
  return param_1;
}


```

### callee `FUN_08007580` @ `08007580`
```c

int FUN_08007580(uint param_1)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  int iVar5;
  int iVar6;
  uint *puVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  bool bVar11;
  bool bVar12;
  bool bVar13;
  bool bVar14;
  
  HintPreloadData(param_1);
  puVar7 = (uint *)(param_1 & 0xfffffff8);
  HintPreloadData(puVar7 + 8);
  if ((param_1 & 7) != 0) {
    uVar9 = puVar7[1];
    iVar6 = -(param_1 & 7);
    HintPreloadData(puVar7 + 0x10);
    uVar10 = -1 << ((param_1 & 3) << 3);
    uVar8 = *puVar7 | ~uVar10;
    if ((param_1 & 4) == 0) goto LAB_080075b0;
    uVar9 = uVar9 | ~uVar10;
    uVar8 = 0xffffffff;
    goto LAB_080075b0;
  }
  iVar5 = -8;
  do {
    uVar9 = puVar7[1];
    HintPreloadData(puVar7 + 0x10);
    iVar6 = iVar5 + 8;
    uVar8 = *puVar7;
LAB_080075b0:
    cVar1 = -((char)uVar8 == '\0');
    cVar2 = -((char)(uVar8 >> 8) == '\0');
    cVar3 = -((char)(uVar8 >> 0x10) == '\0');
    cVar4 = -((char)(uVar8 >> 0x18) == '\0');
    uVar8 = CONCAT13(cVar4,CONCAT12(cVar3,CONCAT11(cVar2,cVar1)));
    bVar11 = (char)uVar9 != '\0';
    bVar12 = (char)(uVar9 >> 8) != '\0';
    bVar13 = (char)(uVar9 >> 0x10) != '\0';
    bVar14 = (char)(uVar9 >> 0x18) != '\0';
    uVar9 = CONCAT13(bVar14 * cVar4 - !bVar14,
                     CONCAT12(bVar13 * cVar3 - !bVar13,
                              CONCAT11(bVar12 * cVar2 - !bVar12,bVar11 * cVar1 - !bVar11)));
    iVar5 = iVar6;
    if (uVar9 != 0) break;
    uVar8 = puVar7[2];
    uVar9 = puVar7[3];
    iVar5 = iVar6 + 8;
    cVar1 = -((char)uVar8 == '\0');
    cVar2 = -((char)(uVar8 >> 8) == '\0');
    cVar3 = -((char)(uVar8 >> 0x10) == '\0');
    cVar4 = -((char)(uVar8 >> 0x18) == '\0');
    uVar8 = CONCAT13(cVar4,CONCAT12(cVar3,CONCAT11(cVar2,cVar1)));
    bVar11 = (char)uVar9 != '\0';
    bVar12 = (char)(uVar9 >> 8) != '\0';
    bVar13 = (char)(uVar9 >> 0x10) != '\0';
    bVar14 = (char)(uVar9 >> 0x18) != '\0';
    uVar9 = CONCAT13(bVar14 * cVar4 - !bVar14,
                     CONCAT12(bVar13 * cVar3 - !bVar13,
                              CONCAT11(bVar12 * cVar2 - !bVar12,bVar11 * cVar1 - !bVar11)));
    if (uVar9 != 0) break;
    uVar8 = puVar7[4];
    uVar9 = puVar7[5];
    iVar5 = iVar6 + 0x10;
    cVar1 = -((char)uVar8 == '\0');
    cVar2 = -((char)(uVar8 >> 8) == '\0');
    cVar3 = -((char)(uVar8 >> 0x10) == '\0');
    cVar4 = -((char)(uVar8 >> 0x18) == '\0');
    uVar8 = CONCAT13(cVar4,CONCAT12(cVar3,CONCAT11(cVar2,cVar1)));
    bVar11 = (char)uVar9 != '\0';
    bVar12 = (char)(uVar9 >> 8) != '\0';
    bVar13 = (char)(uVar9 >> 0x10) != '\0';
    bVar14 = (char)(uVar9 >> 0x18) != '\0';
    uVar9 = CONCAT13(bVar14 * cVar4 - !bVar14,
                     CONCAT12(bVar13 * cVar3 - !bVar13,
                              CONCAT11(bVar12 * cVar2 - !bVar12,bVar11 * cVar1 - !bVar11)));
    if (uVar9 != 0) break;
    uVar8 = puVar7[6];
    uVar9 = puVar7[7];
    puVar7 = puVar7 + 8;
    iVar5 = iVar6 + 0x18;
    cVar1 = -((char)uVar8 == '\0');
    cVar2 = -((char)(uVar8 >> 8) == '\0');
    cVar3 = -((char)(uVar8 >> 0x10) == '\0');
    cVar4 = -((char)(uVar8 >> 0x18) == '\0');
    uVar8 = CONCAT13(cVar4,CONCAT12(cVar3,CONCAT11(cVar2,cVar1)));
    bVar11 = (char)uVar9 != '\0';
    bVar12 = (char)(uVar9 >> 8) != '\0';
    bVar13 = (char)(uVar9 >> 0x10) != '\0';
    bVar14 = (char)(uVar9 >> 0x18) != '\0';
    uVar9 = CONCAT13(bVar14 * cVar4 - !bVar14,
                     CONCAT12(bVar13 * cVar3 - !bVar13,
                              CONCAT11(bVar12 * cVar2 - !bVar12,bVar11 * cVar1 - !bVar11)));
  } while (uVar9 == 0);
  if (uVar8 == 0) {
    iVar5 = iVar5 + 4;
    uVar8 = uVar9;
  }
  return iVar5 + ((uint)LZCOUNT(uVar8 << 0x18 | (uVar8 >> 8 & 0xff) << 0x10 |
                                (uVar8 >> 0x10 & 0xff) << 8 | uVar8 >> 0x18) >> 3);
}


```

### callee `FUN_0801d860` @ `0801d860`
```c

void FUN_0801d860(int param_1)

{
  undefined4 uVar1;
  
  if (param_1 == 0x12) {
    uVar1 = 2;
  }
  else {
    uVar1 = 0;
  }
  *DAT_0801d870 = uVar1;
  return;
}


```

### callee `FUN_08051058` @ `08051058`
```c

undefined4 FUN_08051058(undefined *param_1,byte *param_2,int param_3)

{
  byte bVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  byte *pbVar5;
  byte bVar6;
  undefined *puVar7;
  undefined *puVar8;
  byte *local_10;
  undefined *local_c;
  
  puVar3 = DAT_080510ec;
  puVar2 = DAT_080510e8;
  if (param_2 == (byte *)0x0) {
LAB_0805108c:
    uVar4 = 0xb;
  }
  else {
    bVar1 = *param_2;
    pbVar5 = param_2;
    bVar6 = bVar1;
    if ((bVar1 < 0x20) || (bVar1 == 0x3a)) {
LAB_08051096:
      if (bVar6 == 0x3a) goto LAB_08051080;
    }
    else {
      do {
        pbVar5 = pbVar5 + 1;
        bVar6 = *pbVar5;
        if (bVar6 < 0x20) goto LAB_08051096;
      } while (bVar6 != 0x3a);
LAB_08051080:
      if ((pbVar5 != param_2 + 1) || (bVar1 != 0x30)) goto LAB_0805108c;
    }
    puVar7 = (undefined *)*DAT_080510e8;
    if (puVar7 != (undefined *)0x0) {
      if (puVar7 == (undefined *)*DAT_080510ec) {
        *DAT_080510ec = 0;
        puVar8 = (undefined *)puVar3[4];
      }
      else {
        puVar8 = (undefined *)DAT_080510ec[4];
      }
      if (puVar8 == puVar7) {
        puVar3[4] = 0;
      }
      *puVar7 = 0;
    }
    if (param_1 == (undefined *)0x0) {
      *puVar2 = 0;
      return 0;
    }
    uVar4 = 0;
    *puVar2 = param_1;
    *param_1 = 0;
    if (param_3 == 1) {
      local_10 = param_2;
      local_c = param_1;
      uVar4 = FUN_0804e3ac(&local_10,&local_c,0);
      return uVar4;
    }
  }
  return uVar4;
}


```

### callee `FUN_0804cb68` @ `0804cb68`
```c

void FUN_0804cb68(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 *local_1c [3];
  undefined4 uStack_10;
  undefined4 uStack_c;
  undefined4 uStack_8;
  undefined4 uStack_4;
  
  local_1c[0] = &uStack_c;
  uStack_10 = param_1;
  uStack_c = param_2;
  uStack_8 = param_3;
  uStack_4 = param_4;
  FUN_080537e0(0,param_1,local_1c);
  return;
}


```

### callee `FUN_08056a38` @ `08056a38`
```c

int FUN_08056a38(uint *param_1,uint *param_2,uint param_3)

{
  uint uVar1;
  uint uVar2;
  uint *puVar3;
  
  if (param_3 == 0) {
    return 0;
  }
  if ((((uint)param_1 | (uint)param_2) & 3) == 0) {
    do {
      if (param_3 < 4) goto LAB_08056a48;
      uVar1 = *param_1;
      if (uVar1 != *param_2) {
        uVar1 = (uint)*(byte *)param_1;
        uVar2 = (uint)*(byte *)param_2;
        puVar3 = param_1;
        if (uVar1 != uVar2) goto LAB_08056ab2;
        goto LAB_08056a58;
      }
      param_3 = param_3 - 4;
    } while ((param_3 != 0) &&
            (param_2 = param_2 + 1, param_1 = param_1 + 1,
            (uVar1 + 0xfefefeff & ~uVar1 & 0x80808080) == 0));
  }
  else {
LAB_08056a48:
    uVar1 = (uint)*(byte *)param_1;
    uVar2 = (uint)*(byte *)param_2;
    if (uVar2 != uVar1) {
LAB_08056ab2:
      return uVar1 - uVar2;
    }
    puVar3 = param_1;
    if (param_3 != 1) {
LAB_08056a58:
      do {
        if (uVar1 == 0) {
          return 0;
        }
        param_1 = (uint *)((int)param_1 + 1);
        uVar1 = (uint)*(byte *)param_1;
        param_2 = (uint *)((int)param_2 + 1);
        uVar2 = (uint)*(byte *)param_2;
        if (uVar1 != uVar2) goto LAB_08056ab2;
      } while ((byte *)((int)puVar3 + ~(uint)param_1 + param_3) != (byte *)0x0);
    }
  }
  return 0;
}


```

### callee `FUN_080513f8` @ `080513f8`
```c

byte FUN_080513f8(char **param_1,undefined4 *param_2,uint param_3,int *param_4)

{
  byte bVar1;
  char *pcVar2;
  int iVar3;
  char *pcVar4;
  undefined4 *puVar5;
  uint *puVar6;
  char **ppcVar7;
  char **ppcVar8;
  char **ppcVar9;
  uint uVar10;
  undefined4 *puVar11;
  undefined4 *puVar12;
  char **ppcVar13;
  byte bVar14;
  undefined4 *puVar15;
  char **ppcVar16;
  char **ppcVar17;
  char *pcVar18;
  uint uVar19;
  undefined4 *puVar20;
  uint uVar21;
  
  *param_4 = 0;
  if ((((param_1 == (char **)0x0) || (pcVar2 = *param_1, pcVar2 == (char *)0x0)) ||
      (*pcVar2 == '\0')) ||
     ((*(short *)(param_1 + 1) != *(short *)(pcVar2 + 6) ||
      (iVar3 = FUN_08052c2c(pcVar2[1]), iVar3 << 0x1f < 0)))) {
    bVar14 = 9;
  }
  else {
    bVar14 = *(byte *)((int)param_1 + 0x15);
    if (bVar14 == 0) {
      bVar1 = *(byte *)(param_1 + 5);
      if ((bVar1 & 1) == 0) {
        bVar14 = 7;
      }
      else {
        pcVar2 = param_1[6];
        if ((uint)((int)param_1[3] - (int)pcVar2) <= param_3) {
          param_3 = (int)param_1[3] - (int)pcVar2;
        }
        if (param_3 != 0) {
          ppcVar9 = param_1 + 0xc;
          pcVar18 = *param_1;
          do {
            uVar10 = (uint)pcVar2 & 0x1ff;
            if (uVar10 == 0) {
              uVar10 = *(ushort *)(pcVar18 + 10) - 1 & (uint)pcVar2 >> 9;
              if (uVar10 == 0) {
                if (pcVar2 == (char *)0x0) {
                  pcVar2 = param_1[2];
                }
                else if (param_1[0xb] == (char *)0x0) {
                  pcVar2 = (char *)FUN_0804e7d8(*param_1,param_1[7]);
                }
                else {
                  puVar6 = (uint *)(param_1[0xb] + 4);
                  uVar21 = ((uint)pcVar2 >> 9) / (uint)*(ushort *)(*param_1 + 10);
                  uVar19 = *puVar6;
                  while( true ) {
                    if (uVar19 == 0) goto LAB_08051652;
                    if (uVar21 < uVar19) break;
                    uVar21 = uVar21 - uVar19;
                    puVar6 = puVar6 + 2;
                    uVar19 = *puVar6;
                  }
                  pcVar2 = (char *)(puVar6[1] + uVar21);
                }
                if (pcVar2 < &UNK_00000002) goto LAB_08051652;
                if (pcVar2 == (char *)0xffffffff) goto LAB_0805168a;
                iVar3 = *(int *)(pcVar18 + 0x1c);
                pcVar4 = pcVar2 + -2;
                param_1[7] = pcVar2;
                if ((char *)(iVar3 + -2) <= pcVar4) goto LAB_08051652;
              }
              else {
                pcVar4 = param_1[7] + -2;
                if ((char *)(*(int *)(pcVar18 + 0x1c) + -2) <= pcVar4) goto LAB_08051652;
              }
              uVar21 = (uint)*(ushort *)(pcVar18 + 10);
              iVar3 = uVar21 * (int)pcVar4 + *(int *)(pcVar18 + 0x30);
              if (iVar3 == 0) {
LAB_08051652:
                *(undefined *)((int)param_1 + 0x15) = 2;
                return 2;
              }
              pcVar2 = (char *)(iVar3 + uVar10);
              if (param_3 < 0x200) {
                if (param_1[8] != pcVar2) {
                  if (*(char *)(param_1 + 5) < '\0') {
                    iVar3 = FUN_08052c80(pcVar18[1],ppcVar9,param_1[8],1);
                    if (iVar3 != 0) goto LAB_0805168a;
                    *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0x7f;
                  }
                  iVar3 = FUN_08052c64(pcVar18[1],ppcVar9,pcVar2,1);
                  if (iVar3 != 0) goto LAB_0805168a;
                }
                param_1[8] = pcVar2;
                uVar10 = (uint)param_1[6] & 0x1ff;
                goto LAB_08051520;
              }
              uVar19 = param_3 >> 9;
              if (uVar21 < uVar10 + (param_3 >> 9)) {
                uVar19 = uVar21 - uVar10;
              }
              iVar3 = FUN_08052c64(pcVar18[1],param_2,pcVar2,uVar19);
              if (iVar3 != 0) {
LAB_0805168a:
                *(undefined *)((int)param_1 + 0x15) = 1;
                return bVar1 & 1;
              }
              if ((*(char *)(param_1 + 5) < '\0') &&
                 ((uint)((int)param_1[8] - (int)pcVar2) < uVar19)) {
                ppcVar16 = (char **)(param_2 + ((int)param_1[8] - (int)pcVar2) * 0x80);
                if ((uint)((int)ppcVar16 - ((int)param_1 + 0x31)) < 3) {
                  ppcVar17 = param_1 + 0x8c;
                  ppcVar13 = (char **)((int)ppcVar16 + -1);
                  uVar10 = (int)ppcVar17 - (int)ppcVar9 & 7;
                  ppcVar7 = ppcVar9;
                  if (uVar10 != 0) {
                    ppcVar8 = ppcVar9;
                    if (uVar10 != 1) {
                      if (uVar10 != 2) {
                        if (uVar10 != 3) {
                          if (uVar10 != 4) {
                            if (uVar10 != 5) {
                              if (uVar10 != 6) {
                                ppcVar7 = (char **)((int)param_1 + 0x31);
                                *(undefined *)ppcVar16 = *(undefined *)ppcVar9;
                                ppcVar13 = ppcVar16;
                              }
                              ppcVar8 = (char **)((int)ppcVar7 + 1);
                              ppcVar13 = (char **)((int)ppcVar13 + 1);
                              *(undefined *)ppcVar13 = *(undefined *)ppcVar7;
                            }
                            ppcVar7 = (char **)((int)ppcVar8 + 1);
                            ppcVar13 = (char **)((int)ppcVar13 + 1);
                            *(undefined *)ppcVar13 = *(undefined *)ppcVar8;
                          }
                          ppcVar8 = (char **)((int)ppcVar7 + 1);
                          ppcVar13 = (char **)((int)ppcVar13 + 1);
                          *(undefined *)ppcVar13 = *(undefined *)ppcVar7;
                        }
                        ppcVar7 = (char **)((int)ppcVar8 + 1);
                        ppcVar13 = (char **)((int)ppcVar13 + 1);
                        *(undefined *)ppcVar13 = *(undefined *)ppcVar8;
                      }
                      ppcVar8 = (char **)((int)ppcVar7 + 1);
                      ppcVar13 = (char **)((int)ppcVar13 + 1);
                      *(undefined *)ppcVar13 = *(undefined *)ppcVar7;
                    }
                    ppcVar13 = (char **)((int)ppcVar13 + 1);
                    *(undefined *)ppcVar13 = *(undefined *)ppcVar8;
                    ppcVar7 = (char **)((int)ppcVar8 + 1);
                    if (ppcVar17 == (char **)((int)ppcVar8 + 1)) goto LAB_080514d8;
                  }
                  do {
                    ppcVar16 = ppcVar7 + 2;
                    *(undefined *)((int)ppcVar13 + 1) = *(undefined *)ppcVar7;
                    *(undefined *)((int)ppcVar13 + 2) = *(undefined *)((int)ppcVar7 + 1);
                    *(undefined *)((int)ppcVar13 + 3) = *(undefined *)((int)ppcVar7 + 2);
                    *(undefined *)(ppcVar13 + 1) = *(undefined *)((int)ppcVar7 + 3);
                    *(undefined *)((int)ppcVar13 + 5) = *(undefined *)(ppcVar7 + 1);
                    *(undefined *)((int)ppcVar13 + 6) = *(undefined *)((int)ppcVar7 + 5);
                    *(undefined *)((int)ppcVar13 + 7) = *(undefined *)((int)ppcVar7 + 6);
                    ppcVar13 = ppcVar13 + 2;
                    *(undefined *)ppcVar13 = *(undefined *)((int)ppcVar7 + 7);
                    ppcVar7 = ppcVar16;
                  } while (ppcVar17 != ppcVar16);
                }
                else {
                  ppcVar13 = ppcVar9;
                  ppcVar7 = ppcVar16;
                  do {
                    ppcVar17 = ppcVar7 + 8;
                    *ppcVar7 = *ppcVar13;
                    ppcVar7[1] = ppcVar13[1];
                    ppcVar7[2] = ppcVar13[2];
                    ppcVar7[3] = ppcVar13[3];
                    ppcVar7[4] = ppcVar13[4];
                    ppcVar7[5] = ppcVar13[5];
                    ppcVar7[6] = ppcVar13[6];
                    ppcVar7[7] = ppcVar13[7];
                    ppcVar13 = ppcVar13 + 8;
                    ppcVar7 = ppcVar17;
                  } while (ppcVar17 != ppcVar16 + 0x80);
                }
              }
LAB_080514d8:
              uVar19 = uVar19 << 9;
            }
            else {
LAB_08051520:
              puVar11 = (undefined4 *)(uVar10 + (int)ppcVar9);
              uVar19 = 0x200 - uVar10;
              if (param_3 <= 0x200 - uVar10) {
                uVar19 = param_3;
              }
              uVar21 = uVar19 - 1;
              if (((int)param_2 - (uVar10 + 1 + (int)ppcVar9) < 3) || (uVar21 < 8)) {
                uVar10 = uVar19 & 7;
                puVar20 = (undefined4 *)((int)param_2 + -1);
                puVar15 = (undefined4 *)((int)puVar11 + uVar19);
                puVar12 = puVar11;
                if (uVar10 != 0) {
                  if (uVar10 != 1) {
                    if (uVar10 != 2) {
                      if (uVar10 != 3) {
                        if (uVar10 != 4) {
                          if (uVar10 != 5) {
                            if (uVar10 != 6) {
                              puVar12 = (undefined4 *)((int)puVar11 + 1);
                              *(undefined *)param_2 = *(undefined *)puVar11;
                              puVar20 = param_2;
                            }
                            puVar11 = (undefined4 *)((int)puVar12 + 1);
                            puVar20 = (undefined4 *)((int)puVar20 + 1);
                            *(undefined *)puVar20 = *(undefined *)puVar12;
                          }
                          puVar12 = (undefined4 *)((int)puVar11 + 1);
                          puVar20 = (undefined4 *)((int)puVar20 + 1);
                          *(undefined *)puVar20 = *(undefined *)puVar11;
                        }
                        puVar11 = (undefined4 *)((int)puVar12 + 1);
                        puVar20 = (undefined4 *)((int)puVar20 + 1);
                        *(undefined *)puVar20 = *(undefined *)puVar12;
                      }
                      puVar12 = (undefined4 *)((int)puVar11 + 1);
                      puVar20 = (undefined4 *)((int)puVar20 + 1);
                      *(undefined *)puVar20 = *(undefined *)puVar11;
                    }
                    puVar11 = (undefined4 *)((int)puVar12 + 1);
                    puVar20 = (undefined4 *)((int)puVar20 + 1);
                    *(undefined *)puVar20 = *(undefined *)puVar12;
                  }
                  puVar20 = (undefined4 *)((int)puVar20 + 1);
                  *(undefined *)puVar20 = *(undefined *)puVar11;
                  puVar12 = (undefined4 *)((int)puVar11 + 1);
                  if ((undefined4 *)((int)puVar11 + 1) == puVar15) goto LAB_080514dc;
                }
                do {
                  puVar11 = puVar12 + 2;
                  *(undefined *)((int)puVar20 + 1) = *(undefined *)puVar12;
                  *(undefined *)((int)puVar20 + 2) = *(undefined *)((int)puVar12 + 1);
                  *(undefined *)((int)puVar20 + 3) = *(undefined *)((int)puVar12 + 2);
                  *(undefined *)(puVar20 + 1) = *(undefined *)((int)puVar12 + 3);
                  *(undefined *)((int)puVar20 + 5) = *(undefined *)(puVar12 + 1);
                  *(undefined *)((int)puVar20 + 6) = *(undefined *)((int)puVar12 + 5);
                  *(undefined *)((int)puVar20 + 7) = *(undefined *)((int)puVar12 + 6);
                  puVar20 = puVar20 + 2;
                  *(undefined *)puVar20 = *(undefined *)((int)puVar12 + 7);
                  puVar12 = puVar11;
                } while (puVar11 != puVar15);
              }
              else {
                uVar10 = ((uVar19 & 0xfffffffc) - 4 >> 2) + 1 & 7;
                puVar20 = puVar11;
                puVar12 = param_2;
                if (uVar10 == 0) goto LAB_080515e8;
                if (uVar10 != 1) {
                  puVar15 = puVar11;
                  puVar5 = param_2;
                  if (uVar10 != 2) {
                    if (uVar10 != 3) {
                      if (uVar10 != 4) {
                        if (uVar10 != 5) {
                          if (uVar10 != 6) {
                            puVar15 = puVar11 + 1;
                            puVar5 = param_2 + 1;
                            *param_2 = *puVar11;
                          }
                          puVar20 = puVar15 + 1;
                          puVar12 = puVar5 + 1;
                          *puVar5 = *puVar15;
                        }
                        puVar15 = puVar20 + 1;
                        puVar5 = puVar12 + 1;
                        *puVar12 = *puVar20;
                      }
                      puVar20 = puVar15 + 1;
                      puVar12 = puVar5 + 1;
                      *puVar5 = *puVar15;
                    }
                    puVar15 = puVar20 + 1;
                    puVar5 = puVar12 + 1;
                    *puVar12 = *puVar20;
                  }
                  puVar20 = puVar15 + 1;
                  puVar12 = puVar5 + 1;
                  *puVar5 = *puVar15;
                }
                *puVar12 = *puVar20;
                puVar20 = puVar20 + 1;
                for (puVar12 = puVar12 + 1;
                    (undefined4 *)((uVar19 & 0xfffffffc) + (int)param_2) != puVar12;
                    puVar12 = puVar12 + 8) {
LAB_080515e8:
                  *puVar12 = *puVar20;
                  puVar12[1] = puVar20[1];
                  puVar12[2] = puVar20[2];
                  puVar12[3] = puVar20[3];
                  puVar12[4] = puVar20[4];
                  puVar12[5] = puVar20[5];
                  puVar12[6] = puVar20[6];
                  puVar12[7] = puVar20[7];
                  puVar20 = puVar20 + 8;
                }
                uVar10 = uVar19 & 0xfffffffc;
                if (uVar19 != uVar10) {
                  *(undefined *)((int)param_2 + uVar10) = *(undefined *)((int)puVar11 + uVar10);
                  if ((uVar21 != uVar10) &&
                     (*(undefined *)((int)param_2 + uVar10 + 1) =
                           *(undefined *)((int)puVar11 + uVar10 + 1), uVar21 - uVar10 != 1)) {
                    *(undefined *)((int)param_2 + uVar10 + 2) =
                         *(undefined *)((int)puVar11 + uVar10 + 2);
                  }
                }
              }
            }
LAB_080514dc:
            param_3 = param_3 - uVar19;
            iVar3 = *param_4;
            param_2 = (undefined4 *)((int)param_2 + uVar19);
            pcVar2 = param_1[6] + uVar19;
            param_1[6] = pcVar2;
            *param_4 = iVar3 + uVar19;
          } while (param_3 != 0);
        }
      }
    }
  }
  return bVar14;
}


```

### callee `FUN_08056428` @ `08056428`
```c

void FUN_08056428(undefined4 *param_1,undefined param_2,uint param_3)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  uint uVar3;
  undefined4 uVar4;
  bool bVar5;
  
  if (((uint)param_1 & 3) != 0) {
    uVar3 = param_3 - 1;
    puVar1 = param_1;
    if (param_3 == 0) {
      return;
    }
    while( true ) {
      param_1 = (undefined4 *)((int)puVar1 + 1);
      *(undefined *)puVar1 = param_2;
      param_3 = uVar3;
      if (((uint)param_1 & 3) == 0) break;
      bVar5 = uVar3 == 0;
      uVar3 = uVar3 - 1;
      puVar1 = param_1;
      if (bVar5) {
        return;
      }
    }
  }
  if (3 < param_3) {
    uVar4 = CONCAT22(CONCAT11(param_2,param_2),CONCAT11(param_2,param_2));
    if (0xf < param_3) {
      puVar1 = param_1 + 4;
      do {
        puVar1[-4] = uVar4;
        puVar1[-3] = uVar4;
        puVar1[-2] = uVar4;
        puVar1[-1] = uVar4;
        puVar1 = puVar1 + 4;
      } while (puVar1 != (undefined4 *)((int)param_1 + (param_3 - 0x10 & 0xfffffff0) + 0x20));
      uVar3 = param_3 & 0xc;
      param_1 = param_1 + ((param_3 - 0x10 >> 4) + 1) * 4;
      param_3 = param_3 & 0xf;
      if (uVar3 == 0) goto joined_r0x080564a6;
    }
    puVar1 = (undefined4 *)((param_3 - 4 & 0xfffffffc) + 4 + (int)param_1);
    do {
      puVar2 = param_1 + 1;
      *param_1 = uVar4;
      param_1 = puVar2;
    } while (puVar1 != puVar2);
    param_3 = param_3 & 3;
    param_1 = puVar1;
  }
joined_r0x080564a6:
  if (param_3 != 0) {
    puVar1 = param_1;
    do {
      puVar2 = (undefined4 *)((int)puVar1 + 1);
      *(undefined *)puVar1 = param_2;
      puVar1 = puVar2;
    } while ((undefined4 *)(param_3 + (int)param_1) != puVar2);
  }
  return;
}


```

### callee `FUN_0805241c` @ `0805241c`
```c

int FUN_0805241c(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 local_4c [2];
  undefined auStack_44 [47];
  char local_15;
  
  local_4c[0] = param_1;
  iVar1 = FUN_0804e3ac(local_4c,auStack_44,0);
  if ((iVar1 == 0) && (iVar1 = FUN_0804fc10(auStack_44,local_4c[0]), iVar1 == 0)) {
    if (local_15 < '\0') {
      iVar1 = 6;
    }
    else if (param_2 != 0) {
      FUN_0804debc(auStack_44,param_2);
    }
  }
  return iVar1;
}


```

### callee `FUN_08051f1c` @ `08051f1c`
```c

char FUN_08051f1c(char **param_1,char *param_2)

{
  char cVar1;
  int iVar2;
  uint *puVar3;
  char *pcVar4;
  char **ppcVar5;
  int iVar6;
  char *pcVar7;
  char *pcVar8;
  uint uVar9;
  char *pcVar10;
  char *pcVar11;
  uint uVar12;
  uint uVar13;
  uint *local_38;
  
  if ((((param_1 == (char **)0x0) || (pcVar7 = *param_1, pcVar7 == (char *)0x0)) ||
      (*pcVar7 == '\0')) ||
     ((*(short *)(param_1 + 1) != *(short *)(pcVar7 + 6) ||
      (iVar2 = FUN_08052c2c(pcVar7[1]), iVar2 << 0x1f < 0)))) {
    return '\t';
  }
  pcVar7 = *param_1;
  if (*(char *)((int)param_1 + 0x15) != '\0') {
    return *(char *)((int)param_1 + 0x15);
  }
  puVar3 = (uint *)param_1[0xb];
  if (puVar3 == (uint *)0x0) {
    if ((param_1[3] < param_2) && ((*(byte *)(param_1 + 5) & 2) == 0)) {
      param_2 = param_1[3];
    }
    pcVar8 = param_1[6];
    param_1[6] = (char *)0x0;
    if (param_2 == (char *)0x0) {
      return '\0';
    }
    uVar13 = (uint)*(ushort *)(pcVar7 + 10);
    pcVar4 = (char *)(uVar13 * 0x200);
    if ((pcVar8 == (char *)0x0) ||
       (pcVar8 = pcVar8 + -1, (uint)(param_2 + -1) / (uint)pcVar4 < (uint)pcVar8 / (uint)pcVar4)) {
      pcVar10 = param_1[2];
      if (pcVar10 == (char *)0x0) {
        pcVar10 = (char *)FUN_0804f088(param_1,0);
        if (pcVar10 == &UNK_00000001) goto LAB_0805215c;
        if (pcVar10 == (char *)0xffffffff) goto LAB_08052154;
        pcVar8 = param_1[6];
        param_1[2] = pcVar10;
      }
      else {
        pcVar8 = (char *)0x0;
      }
      param_1[7] = pcVar10;
    }
    else {
      pcVar10 = param_1[7];
      pcVar8 = (char *)((uint)pcVar8 & uVar13 * -0x200);
      param_2 = param_2 + -(int)pcVar8;
      param_1[6] = pcVar8;
    }
    if (pcVar10 != (char *)0x0) {
      if (pcVar4 < param_2) {
        while( true ) {
          param_2 = param_2 + uVar13 * -0x200;
          param_1[6] = pcVar8 + (int)pcVar4;
          if ((int)((uint)*(byte *)(param_1 + 5) << 0x1e) < 0) {
            pcVar10 = (char *)FUN_0804f088(param_1,pcVar10);
            if (pcVar10 == (char *)0x0) {
              pcVar8 = param_1[6];
              pcVar10 = (char *)0x0;
              goto LAB_080521e2;
            }
          }
          else {
            pcVar10 = (char *)FUN_0804e7d8(*param_1);
          }
          if (pcVar10 == (char *)0xffffffff) goto LAB_08052154;
          if ((pcVar10 < &UNK_00000002) || (*(char **)(pcVar7 + 0x1c) <= pcVar10))
          goto LAB_0805215c;
          param_1[7] = pcVar10;
          if (param_2 <= pcVar4) break;
          pcVar8 = param_1[6];
        }
        pcVar8 = param_1[6];
      }
      pcVar8 = pcVar8 + (int)param_2;
      param_1[6] = pcVar8;
      if (((uint)param_2 & 0x1ff) == 0) {
        pcVar10 = (char *)0x0;
      }
      else {
        if (((char *)(*(int *)(pcVar7 + 0x1c) + -2) <= pcVar10 + -2) ||
           (iVar2 = (int)(pcVar10 + -2) * (uint)*(ushort *)(pcVar7 + 10) + *(int *)(pcVar7 + 0x30),
           iVar2 == 0)) goto LAB_0805215c;
        pcVar10 = (char *)(iVar2 + ((uint)param_2 >> 9));
      }
    }
LAB_080521e2:
    if (param_1[3] < pcVar8) {
      param_1[3] = pcVar8;
      *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) | 0x40;
    }
    if (((uint)pcVar8 & 0x1ff) == 0) {
      return '\0';
    }
    pcVar8 = param_1[8];
    if (pcVar8 == pcVar10) {
      return '\0';
    }
  }
  else {
    if (param_2 == (char *)0xffffffff) {
      local_38 = puVar3 + 1;
      uVar13 = *puVar3;
      if (param_1[2] != (char *)0x0) {
        uVar12 = 2;
        pcVar8 = pcVar7;
        pcVar4 = param_1[2];
LAB_080520bc:
        uVar9 = 0;
        pcVar10 = pcVar4;
        do {
          uVar9 = uVar9 + 1;
          if ((pcVar10 < &UNK_00000002) || (*(char **)(pcVar8 + 0x1c) <= pcVar10)) {
LAB_080520ce:
            *(undefined *)((int)param_1 + 0x15) = 2;
            return '\x02';
          }
          cVar1 = *pcVar8;
          if (cVar1 == '\x02') {
            if ((*(int *)(pcVar8 + 0x28) + ((uint)pcVar10 >> 8) != *(int *)(pcVar8 + 0x34)) &&
               (iVar2 = FUN_0804e200(pcVar8), iVar2 != 0)) goto LAB_08052154;
            pcVar11 = (char *)(uint)*(ushort *)(pcVar8 + ((uint)pcVar10 & 0xff) * 2 + 0x38);
          }
          else if (cVar1 == '\x03') {
            if ((*(int *)(pcVar8 + 0x28) + ((uint)pcVar10 >> 7) != *(int *)(pcVar8 + 0x34)) &&
               (iVar2 = FUN_0804e200(pcVar8), iVar2 != 0)) goto LAB_08052154;
            pcVar11 = (char *)(*(uint *)(pcVar8 + ((uint)pcVar10 & 0x7f) * 4 + 0x38) & 0xfffffff);
          }
          else {
            if (cVar1 != '\x01') goto LAB_080520ce;
            pcVar11 = pcVar10 + ((uint)pcVar10 >> 1);
            iVar6 = *(int *)(pcVar8 + 0x28);
            iVar2 = *(int *)(pcVar8 + 0x34);
            if (iVar6 + ((uint)pcVar11 >> 9) != iVar2) {
              iVar2 = FUN_0804e200(pcVar8);
              if (iVar2 != 0) goto LAB_08052154;
              iVar6 = *(int *)(pcVar8 + 0x28);
              iVar2 = *(int *)(pcVar8 + 0x34);
            }
            cVar1 = pcVar8[((uint)pcVar11 & 0x1ff) + 0x38];
            if ((iVar6 + ((uint)(pcVar11 + 1) >> 9) != iVar2) &&
               (iVar2 = FUN_0804e200(pcVar8), iVar2 != 0)) goto LAB_08052154;
            if ((int)pcVar10 << 0x1f < 0) {
              pcVar11 = (char *)(uint)(ushort)(CONCAT11(pcVar8[((uint)(pcVar11 + 1) & 0x1ff) + 0x38]
                                                        ,cVar1) >> 4);
            }
            else {
              pcVar11 = (char *)(CONCAT11(pcVar8[((uint)(pcVar11 + 1) & 0x1ff) + 0x38],cVar1) &
                                0xfff);
            }
          }
          if (pcVar11 < &UNK_00000002) goto LAB_080520ce;
          if (pcVar10 + 1 != pcVar11) goto LAB_08052208;
          pcVar8 = *param_1;
          pcVar10 = pcVar11;
        } while( true );
      }
      uVar12 = 2;
      goto LAB_080521b2;
    }
    if (param_1[3] <= param_2) {
      param_2 = param_1[3];
    }
    param_1[6] = param_2;
    if (param_2 == (char *)0x0) {
      return '\0';
    }
    uVar13 = (uint)*(ushort *)(pcVar7 + 10);
    pcVar8 = (char *)puVar3[1];
    ppcVar5 = (char **)(puVar3 + 1);
    pcVar4 = (char *)(((uint)(param_2 + -1) >> 9) / uVar13);
    if (pcVar8 == (char *)0x0) {
      pcVar8 = (char *)0x0;
    }
    else {
      do {
        if (pcVar4 < pcVar8) {
          pcVar8 = ppcVar5[1] + (int)pcVar4;
          pcVar4 = pcVar8 + -2;
          goto LAB_08051fa2;
        }
        pcVar4 = pcVar4 + -(int)pcVar8;
        ppcVar5 = ppcVar5 + 2;
        pcVar8 = *ppcVar5;
      } while (pcVar8 != (char *)0x0);
    }
    pcVar4 = (char *)0xfffffffe;
LAB_08051fa2:
    iVar2 = *(int *)(pcVar7 + 0x1c);
    param_1[7] = pcVar8;
    if (((char *)(iVar2 + -2) <= pcVar4) ||
       (iVar2 = (int)pcVar4 * uVar13 + *(int *)(pcVar7 + 0x30), iVar2 == 0)) {
LAB_0805215c:
      *(undefined *)((int)param_1 + 0x15) = 2;
      return '\x02';
    }
    if (((uint)param_2 & 0x1ff) == 0) {
      return '\0';
    }
    pcVar8 = param_1[8];
    pcVar10 = (char *)(((uint)(param_2 + -1) >> 9 & uVar13 - 1) + iVar2);
    if (pcVar8 == pcVar10) {
      return '\0';
    }
  }
  if (*(char *)(param_1 + 5) < '\0') {
    iVar2 = FUN_08052c80(pcVar7[1],param_1 + 0xc,pcVar8,1);
    if (iVar2 != 0) goto LAB_08052154;
    *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0x7f;
  }
  iVar2 = FUN_08052c64(pcVar7[1],param_1 + 0xc,pcVar10,1);
  if (iVar2 == 0) {
    param_1[8] = pcVar10;
    return '\0';
  }
LAB_08052154:
  *(undefined *)((int)param_1 + 0x15) = 1;
  return '\x01';
LAB_08052208:
  uVar12 = uVar12 + 2;
  if (uVar13 < uVar12) {
    pcVar8 = *(char **)(pcVar7 + 0x1c);
  }
  else {
    *local_38 = uVar9;
    local_38[1] = (uint)pcVar4;
    pcVar8 = *(char **)(pcVar7 + 0x1c);
    local_38 = local_38 + 2;
  }
  if (pcVar8 <= pcVar11) goto LAB_08052268;
  pcVar8 = *param_1;
  pcVar4 = pcVar11;
  goto LAB_080520bc;
LAB_08052268:
  puVar3 = (uint *)param_1[0xb];
LAB_080521b2:
  *puVar3 = uVar12;
  if (uVar12 <= uVar13) {
    *local_38 = 0;
    return '\0';
  }
  return '\x11';
}


```

### callee `FUN_080569f8` @ `080569f8`
```c

void FUN_080569f8(undefined *param_1,undefined4 param_2)

{
  undefined *local_80 [2];
  undefined4 local_78;
  undefined4 local_74;
  undefined *local_70;
  undefined4 uStack_6c;
  
  uStack_6c = 0x7fffffff;
  local_78 = 0x7fffffff;
  local_74 = DAT_08056a34;
  local_80[0] = param_1;
  local_70 = param_1;
  FUN_08056c90(*DAT_08056a30,local_80,param_2);
  *local_80[0] = 0;
  return;
}


```

### callee `FUN_080510f0` @ `080510f0`
```c

int FUN_080510f0(char **param_1,undefined4 param_2,uint param_3)

{
  undefined2 uVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  int iVar5;
  undefined4 uVar6;
  char *pcVar7;
  uint uVar8;
  uint uVar9;
  char *pcVar10;
  int iVar11;
  char *pcVar12;
  undefined4 local_5c;
  char *local_58;
  char *local_54;
  byte local_4e;
  char *local_4c;
  char *local_40;
  char *local_34;
  char local_25;
  
  if (param_1 == (char **)0x0) {
    return 9;
  }
  uVar9 = param_3 & 0x3f;
  local_5c = param_2;
  iVar5 = FUN_0804e3ac(&local_5c,&local_58,uVar9);
  if (iVar5 != 0) goto LAB_08051114;
  local_54 = local_58;
  iVar5 = FUN_0804fc10(&local_54,local_5c);
  if (iVar5 != 0) {
    if (((param_3 & 0x1c) == 0) || (iVar5 != 4)) goto LAB_08051114;
    if ((*DAT_080513e0 != (char *)0x0) && (DAT_080513e0[4] != (char *)0x0)) goto LAB_0805116c;
    uVar9 = uVar9 | 8;
    iVar5 = FUN_08050238(&local_54);
    if (iVar5 != 0) goto LAB_08051114;
LAB_08051194:
    uVar6 = FUN_0801fefc();
    cVar2 = (char)((uint)uVar6 >> 8);
    local_34[0xf] = cVar2;
    local_34[0xe] = (char)uVar6;
    cVar3 = (char)((uint)uVar6 >> 0x10);
    local_34[0x10] = cVar3;
    cVar4 = (char)((uint)uVar6 >> 0x18);
    local_34[0x11] = cVar4;
    local_34[0x16] = (char)uVar6;
    local_34[0x17] = cVar2;
    local_34[0x18] = cVar3;
    local_34[0x19] = cVar4;
    local_34[0xb] = ' ';
    uVar8 = (uint)*(ushort *)(local_34 + 0x1a);
    if (*local_58 == '\x03') {
      uVar8 = CONCAT22(*(undefined2 *)(local_34 + 0x14),*(ushort *)(local_34 + 0x1a));
    }
    *(undefined2 *)(local_34 + 0x1a) = 0;
    if (*local_58 == '\x03') {
      *(undefined2 *)(local_34 + 0x14) = 0;
    }
    *(undefined4 *)(local_34 + 0x1c) = 0;
    local_58[3] = '\x01';
    if (uVar8 != 0) {
      iVar11 = *(int *)(local_58 + 0x34);
      iVar5 = FUN_08050100(&local_54,uVar8);
      if (iVar5 != 0) goto LAB_08051114;
      if (iVar11 == *(int *)(local_58 + 0x34)) {
        *(uint *)(local_58 + 0x10) = uVar8 - 1;
      }
      else {
        iVar5 = FUN_0804e200(local_58,iVar11);
        *(uint *)(local_58 + 0x10) = uVar8 - 1;
        if (iVar5 != 0) goto LAB_08051114;
      }
    }
LAB_0805121a:
    uVar8 = uVar9 & 0xfffffffe | 0x40;
    uVar9 = uVar9 | 0x40;
    goto LAB_08051222;
  }
  if (local_25 < '\0') {
    iVar5 = 6;
    goto LAB_08051114;
  }
  uVar8 = param_3 & 0x3e;
  pcVar10 = *DAT_080513e0;
  if (pcVar10 != (char *)0x0) {
    if (pcVar10 == local_54) {
      if ((DAT_080513e0[1] == local_4c) && (DAT_080513e0[2] == local_40)) {
        iVar5 = 0;
        goto LAB_08051272;
      }
      if (DAT_080513e0[4] == (char *)0x0) goto LAB_08051284;
      if ((DAT_080513e0[4] == pcVar10) && (DAT_080513e0[5] == local_4c)) {
        pcVar10 = DAT_080513e0[6];
        goto joined_r0x0805126a;
      }
    }
    else {
      if (DAT_080513e0[4] == (char *)0x0) goto LAB_08051284;
      if ((DAT_080513e0[4] == local_54) && (DAT_080513e0[5] == local_4c)) {
        pcVar10 = DAT_080513e0[6];
joined_r0x0805126a:
        if (pcVar10 == local_40) goto LAB_0805126e;
      }
    }
LAB_0805116c:
    iVar5 = 0x12;
    goto LAB_08051114;
  }
  if ((((DAT_080513e0[4] != (char *)0x0) && (local_54 == DAT_080513e0[4])) &&
      (DAT_080513e0[5] == local_4c)) && (local_40 == DAT_080513e0[6])) {
LAB_0805126e:
    iVar5 = 1;
LAB_08051272:
    if ((uVar8 != 0) || (*(short *)(DAT_080513e0 + iVar5 * 4 + 3) == 0x100)) {
      iVar5 = 0x10;
      goto LAB_08051114;
    }
  }
LAB_08051284:
  if ((param_3 & 0x1c) == 0) {
    if ((int)((uint)local_4e << 0x1b) < 0) {
      iVar5 = 4;
      goto LAB_08051114;
    }
    if ((-1 < (int)(param_3 << 0x1e)) || (-1 < (int)((uint)local_4e << 0x1f))) {
      if ((param_3 & 8) != 0) goto LAB_0805121a;
      goto LAB_08051222;
    }
  }
  else if ((local_4e & 0x11) == 0) {
    if ((int)(param_3 << 0x1d) < 0) {
      iVar5 = 8;
      goto LAB_08051114;
    }
    if ((int)(param_3 << 0x1c) < 0) goto LAB_08051194;
LAB_08051222:
    if (uVar8 != 0) {
      uVar8 = 1;
    }
    param_1[9] = *(char **)(local_58 + 0x34);
    param_1[10] = local_34;
    pcVar7 = (char *)FUN_0804de14(&local_54,uVar8);
    pcVar10 = local_58;
    param_1[4] = pcVar7;
    if (pcVar7 != (char *)0x0) {
      pcVar7 = (char *)(uint)*(ushort *)(local_34 + 0x1a);
      if (*local_58 == '\x03') {
        pcVar7 = (char *)CONCAT22(*(undefined2 *)(local_34 + 0x14),*(ushort *)(local_34 + 0x1a));
      }
      uVar1 = *(undefined2 *)(local_58 + 6);
      param_1[2] = pcVar7;
      pcVar12 = *(char **)(local_34 + 0x1c);
      param_1[0xb] = (char *)0x0;
      *(undefined2 *)(param_1 + 1) = uVar1;
      *(undefined *)((int)param_1 + 0x15) = 0;
      param_1[8] = (char *)0x0;
      param_1[6] = (char *)0x0;
      *param_1 = local_58;
      param_1[3] = pcVar12;
      *(char *)(param_1 + 5) = (char)uVar9;
      FUN_08056428(param_1 + 0xc,0,0x200);
      if (-1 < (int)(uVar9 << 0x1a)) {
        return 0;
      }
      if (pcVar12 == (char *)0x0) {
        return 0;
      }
      uVar9 = (uint)*(ushort *)(pcVar10 + 10);
      param_1[6] = pcVar12;
      if ((char *)(uVar9 * 0x200) < pcVar12) {
        do {
          pcVar7 = (char *)FUN_0804e7d8(*param_1,pcVar7);
          pcVar12 = pcVar12 + uVar9 * -0x200;
          if (pcVar7 < &UNK_00000002) {
            iVar5 = 2;
            param_1[7] = pcVar7;
            goto LAB_08051114;
          }
        } while ((pcVar7 != (char *)0xffffffff) && ((char *)(uVar9 * 0x200) < pcVar12));
        param_1[7] = pcVar7;
        if (pcVar7 == (char *)0xffffffff) {
          iVar5 = 1;
          goto LAB_08051114;
        }
      }
      else {
        param_1[7] = pcVar7;
      }
      if (((uint)pcVar12 & 0x1ff) == 0) {
        return 0;
      }
      if ((pcVar7 + -2 < (char *)(*(int *)(local_58 + 0x1c) + -2)) &&
         (iVar5 = (int)(pcVar7 + -2) * (uint)*(ushort *)(local_58 + 10) + *(int *)(local_58 + 0x30),
         iVar5 != 0)) {
        pcVar10 = (char *)(iVar5 + ((uint)pcVar12 >> 9));
        param_1[8] = pcVar10;
        iVar5 = FUN_08052c64(local_58[1],param_1 + 0xc,pcVar10,1);
        if (iVar5 == 0) {
          return 0;
        }
        iVar5 = 1;
        goto LAB_08051114;
      }
    }
    iVar5 = 2;
    goto LAB_08051114;
  }
  iVar5 = 7;
LAB_08051114:
  *param_1 = (char *)0x0;
  return iVar5;
}


```

### callee `FUN_08051d88` @ `08051d88`
```c

int FUN_08051d88(char **param_1)

{
  short sVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  char *pcVar5;
  char *pcVar6;
  char *pcVar7;
  char *pcVar8;
  int iVar9;
  
  if (param_1 == (char **)0x0) {
    return 9;
  }
  pcVar7 = *param_1;
  if ((((pcVar7 == (char *)0x0) || (*pcVar7 == '\0')) ||
      (*(short *)(param_1 + 1) != *(short *)(pcVar7 + 6))) ||
     (iVar2 = FUN_08052c2c(pcVar7[1]), iVar2 << 0x1f < 0)) {
    return 9;
  }
  pcVar7 = *param_1;
  if ((int)((uint)*(byte *)(param_1 + 5) << 0x19) < 0) {
    if ((int)((uint)*(byte *)(param_1 + 5) << 0x18) < 0) {
      iVar2 = FUN_08052c80(pcVar7[1],param_1 + 0xc,param_1[8],1);
      if (iVar2 != 0) {
        return 1;
      }
      *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0x7f;
    }
    uVar3 = FUN_0801fefc();
    if ((param_1[9] != *(char **)(pcVar7 + 0x34)) && (iVar2 = FUN_0804e200(pcVar7), iVar2 != 0)) {
      return iVar2;
    }
    pcVar6 = param_1[10];
    pcVar6[0xb] = pcVar6[0xb] | 0x20;
    pcVar8 = param_1[2];
    pcVar5 = *param_1;
    pcVar6[0x1a] = (char)pcVar8;
    pcVar6[0x1b] = (char)((uint)pcVar8 >> 8);
    if (*pcVar5 == '\x03') {
      pcVar6[0x14] = (char)((uint)pcVar8 >> 0x10);
      pcVar6[0x15] = (char)((uint)pcVar8 >> 0x18);
    }
    pcVar5 = param_1[3];
    pcVar6[0x16] = (char)uVar3;
    pcVar6[0x1c] = (char)pcVar5;
    pcVar6[0x1d] = (char)((uint)pcVar5 >> 8);
    pcVar6[0x1e] = (char)((uint)pcVar5 >> 0x10);
    pcVar6[0x1f] = (char)((uint)pcVar5 >> 0x18);
    pcVar6[0x17] = (char)((uint)uVar3 >> 8);
    pcVar6[0x18] = (char)((uint)uVar3 >> 0x10);
    pcVar6[0x19] = (char)((uint)uVar3 >> 0x18);
    *(undefined2 *)(pcVar6 + 0x12) = 0;
    pcVar7[3] = '\x01';
    iVar2 = FUN_0804ee7c(pcVar7);
    *(byte *)(param_1 + 5) = *(byte *)(param_1 + 5) & 0xbf;
    if (iVar2 != 0) {
      return iVar2;
    }
    pcVar7 = *param_1;
  }
  if (pcVar7 == (char *)0x0) {
    return 9;
  }
  if (*pcVar7 == '\0') {
    return 9;
  }
  if (*(short *)(param_1 + 1) != *(short *)(pcVar7 + 6)) {
    return 9;
  }
  uVar4 = FUN_08052c2c(pcVar7[1]);
  iVar2 = DAT_08051eac;
  if ((uVar4 & 1) != 0) {
    return 9;
  }
  pcVar7 = param_1[4] + -1;
  if (&UNK_00000001 < pcVar7) {
    return 2;
  }
  iVar9 = DAT_08051eac + (int)pcVar7 * 0x10;
  sVar1 = *(short *)(iVar9 + 0xc);
  if (sVar1 == 0x100) {
    *(undefined2 *)(iVar9 + 0xc) = 0;
  }
  else if ((sVar1 != 0) && (*(short *)(iVar9 + 0xc) = sVar1 + -1, sVar1 != 1)) goto LAB_08051e78;
  *(undefined4 *)(iVar2 + (int)pcVar7 * 0x10) = 0;
LAB_08051e78:
  *param_1 = (char *)0x0;
  return 0;
}


```

### callee `FUN_08051eb0` @ `08051eb0`
```c

int FUN_08051eb0(undefined4 param_1)

{
  int iVar1;
  uint uVar2;
  undefined4 local_44;
  char *local_40;
  char *local_3c;
  byte local_36;
  undefined4 local_34;
  int local_1c;
  char local_d;
  
  local_44 = param_1;
  iVar1 = FUN_0804e3ac(&local_44,&local_40,0);
  if (iVar1 == 0) {
    local_3c = local_40;
    iVar1 = FUN_0804fc10(&local_3c,local_44);
    if (iVar1 != 0) {
      if (iVar1 == 4) {
        iVar1 = 5;
      }
      return iVar1;
    }
    iVar1 = 0;
    if (local_d < '\0') {
      *(undefined4 *)(local_40 + 0x18) = local_34;
    }
    else if ((int)((uint)local_36 << 0x1b) < 0) {
      uVar2 = (uint)*(ushort *)(local_1c + 0x1a);
      if (*local_40 == '\x03') {
        uVar2 = CONCAT22(*(undefined2 *)(local_1c + 0x14),*(ushort *)(local_1c + 0x1a));
      }
      *(uint *)(local_40 + 0x18) = uVar2;
    }
    else {
      iVar1 = 5;
    }
  }
  return iVar1;
}


```

---
## `FUN_0801eb38`  @ `0801eb38`
- **Anchors:** Rec%05d.wav
- **Strings seen:** Rec%05d.wav
- **Signature:** `undefined FUN_0801eb38()`
- **Params:** 0  **Calls:** 3 funcs

```c

int FUN_0801eb38(int param_1,int param_2,int param_3)

{
  int iVar1;
  int iVar2;
  undefined auStack_110 [255];
  undefined local_11;
  
  iVar1 = DAT_0801ebd4;
  iVar2 = *(int *)(DAT_0801ebd0 + param_1 * 4);
  if (iVar2 < 1) {
    return DAT_0801ebd8;
  }
  param_2 = param_2 + param_1 * 8;
  param_3 = param_3 + *(int *)(DAT_0801ebd4 + param_2 * 4);
  if (param_3 < 0) {
    iVar2 = 0;
    *(undefined4 *)(DAT_0801ebd4 + param_2 * 4) = 0;
  }
  else {
    iVar2 = iVar2 + -1;
    if (param_3 <= iVar2) {
      iVar2 = param_3;
    }
    *(int *)(DAT_0801ebd4 + param_2 * 4) = iVar2;
  }
  if (param_1 == 1) {
    return DAT_0801ebdc + iVar2 * 0x100;
  }
  if (param_1 == 2) {
    iVar2 = *(int *)(DAT_0801ebe4 + iVar2 * 4);
    if (iVar2 < 0) {
      iVar2 = -iVar2;
    }
    FUN_080569f8(DAT_0801ebec,DAT_0801ebe8,iVar2);
    FUN_08056ab8(auStack_110,DAT_0801ebec,0xff);
    local_11 = 0;
    iVar2 = FUN_08007160(DAT_0801ebf0 + *(int *)(iVar1 + param_2 * 4) * 0x100,auStack_110,0x100);
    return iVar2;
  }
  if (param_1 == 0) {
    return DAT_0801ebe0 + iVar2 * 0x100;
  }
  return DAT_0801ebd8;
}


```

### callee `FUN_08056ab8` @ `08056ab8`
```c

void FUN_08056ab8(uint *param_1,uint *param_2,uint param_3)

{
  char cVar1;
  uint *puVar2;
  uint *puVar3;
  uint uVar5;
  char *pcVar6;
  uint *puVar4;
  
  puVar2 = param_2;
  puVar4 = param_1;
  if (((((uint)param_1 | (uint)param_2) & 3) == 0) && (3 < param_3)) {
    do {
      uVar5 = *param_2;
      puVar2 = param_2;
      puVar4 = param_1;
      if ((uVar5 + 0xfefefeff & ~uVar5 & 0x80808080) != 0) break;
      param_3 = param_3 - 4;
      puVar4 = param_1 + 1;
      *param_1 = uVar5;
      puVar2 = param_2 + 1;
      param_2 = param_2 + 1;
      param_1 = puVar4;
    } while (3 < param_3);
  }
  pcVar6 = (char *)((int)puVar2 - 1);
  do {
    puVar2 = puVar4;
    uVar5 = param_3;
    if (uVar5 == 0) {
      return;
    }
    pcVar6 = pcVar6 + 1;
    cVar1 = *pcVar6;
    *(char *)puVar2 = cVar1;
    param_3 = uVar5 - 1;
    puVar4 = (uint *)((int)puVar2 + 1);
  } while (cVar1 != '\0');
  if (uVar5 - 1 == 0) {
    return;
  }
  do {
    puVar3 = (uint *)((int)puVar4 + 1);
    *(char *)puVar4 = '\0';
    puVar4 = puVar3;
  } while (puVar3 != (uint *)(uVar5 + (int)puVar2));
  return;
}


```

---
## `FUN_0801f0d4`  @ `0801f0d4`
- **Anchors:** /Multigrain/Wavs, SD: /Wavs has, SD: Scan /Wavs
- **Strings seen:** /Multigrain/Wavs | SD: /Wavs has %d wav(s).
 | SD: Scan /Wavs...

- **Signature:** `undefined FUN_0801f0d4()`
- **Params:** 0  **Calls:** 14 funcs

```c

int FUN_0801f0d4(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined auStack_17c [4];
  undefined auStack_178 [4];
  undefined auStack_174 [52];
  undefined auStack_140 [8];
  byte local_138;
  undefined auStack_137 [13];
  char local_12a [262];
  
  FUN_0804cb58(DAT_0801f3b4);
  FUN_08051058(DAT_0801f3bc,DAT_0801f3b8,1);
  iVar4 = FUN_080522b8(auStack_174,DAT_0801f3c0);
  if ((iVar4 != 0) ||
     (iVar4 = FUN_08051eb0(DAT_0801f3c0), iVar7 = DAT_0801f3cc, uVar3 = DAT_0801f3c8,
     iVar2 = DAT_0801f3c4, uVar1 = DAT_0801f3c0, iVar4 != 0)) {
    return iVar4;
  }
  iVar4 = 0x400;
  *(undefined4 *)(DAT_0801f3c4 + 4) = 0;
  while ((iVar5 = FUN_080523c0(auStack_174,auStack_140), iVar5 == 0 && (local_12a[0] != '\0'))) {
    if ((-1 < (int)((uint)local_138 << 0x1e)) &&
       ((((local_12a[0] != '.' && (iVar5 = FUN_08056b1c(auStack_137,0x2e), iVar5 != 0)) &&
         (*(char *)(iVar5 + 1) == 'W')) &&
        ((*(char *)(iVar5 + 2) == 'A' && (*(char *)(iVar5 + 3) == 'V')))))) {
      iVar5 = FUN_0801ee50(local_12a,auStack_17c,auStack_178);
      if (iVar5 == 0) {
        iVar5 = iVar7 + *(int *)(iVar2 + 4) * 0x100;
        *(int *)(iVar2 + 4) = *(int *)(iVar2 + 4) + 1;
        FUN_08056ab8(iVar5,local_12a,0x100);
        *(undefined *)(iVar5 + 0xff) = 0;
        FUN_0804cb68(uVar3,uVar1,local_12a);
      }
      if (*(int *)(iVar2 + 4) == 0x80) break;
    }
    iVar5 = FUN_080523c0(auStack_174,auStack_140);
    if ((iVar5 != 0) || (local_12a[0] == '\0')) break;
    if (((-1 < (int)((uint)local_138 << 0x1e)) &&
        (((local_12a[0] != '.' && (iVar5 = FUN_08056b1c(auStack_137,0x2e), iVar5 != 0)) &&
         (*(char *)(iVar5 + 1) == 'W')))) &&
       ((*(char *)(iVar5 + 2) == 'A' && (*(char *)(iVar5 + 3) == 'V')))) {
      iVar5 = FUN_0801ee50(local_12a,auStack_17c,auStack_178);
      if (iVar5 == 0) {
        iVar5 = iVar7 + *(int *)(iVar2 + 4) * 0x100;
        *(int *)(iVar2 + 4) = *(int *)(iVar2 + 4) + 1;
        FUN_08056ab8(iVar5,local_12a,0x100);
        *(undefined *)(iVar5 + 0xff) = 0;
        FUN_0804cb68(uVar3,uVar1,local_12a);
      }
      if (*(int *)(iVar2 + 4) == 0x80) break;
    }
    iVar4 = iVar4 + -2;
    if (iVar4 == 0) break;
  }
  FUN_0805234c(auStack_174);
  iVar4 = DAT_0801f3cc;
  iVar7 = *(int *)(iVar2 + 4);
  if ((iVar7 != 0) && (iVar5 = DAT_0801f3cc + iVar7 * 0x100, iVar5 != DAT_0801f3cc)) {
    iVar7 = iVar5 - DAT_0801f3cc;
    FUN_0801dd9c(DAT_0801f3cc,iVar5,(0x1f - LZCOUNT(iVar7 >> 8)) * 2);
    if (iVar7 < 0x1001) {
      iVar8 = iVar4 + 0x100;
      iVar7 = iVar4;
      while (iVar5 != iVar8) {
        iVar11 = iVar7 + 0x100;
        iVar8 = FUN_08056a38(iVar11,iVar4,0x100);
        if (iVar8 < 0) {
          FUN_08007160(auStack_140,iVar11,0x100);
          iVar8 = iVar11 - iVar4 >> 8;
          if (0 < iVar11 - iVar4) {
            FUN_08056330(iVar7 + 0x200 + iVar8 * -0x100,iVar11 + iVar8 * -0x100);
          }
          FUN_08007160(iVar4,auStack_140,0x100);
        }
        else {
          FUN_08007160(auStack_140,iVar7 + 0x100,0x100);
          iVar8 = iVar7;
          iVar6 = iVar7 + 0x100;
          while( true ) {
            iVar10 = iVar8;
            iVar8 = FUN_08056a38(auStack_140,iVar10,0x100);
            if (-1 < iVar8) break;
            FUN_08007160(iVar10 + 0x100,iVar10);
            iVar8 = iVar10 + -0x100;
            iVar6 = iVar10;
          }
          FUN_08007160(iVar6,auStack_140,0x100);
        }
        iVar8 = iVar7 + 0x200;
        iVar7 = iVar11;
      }
    }
    else {
      iVar11 = iVar4 + 0x200;
      iVar8 = iVar4;
      iVar7 = iVar4;
      do {
        iVar7 = iVar7 + 0x100;
        iVar10 = iVar8 + 0x100;
        iVar6 = FUN_08056a38(iVar7,iVar4,0x100);
        if (iVar6 < 0) {
          FUN_08007160(auStack_140,iVar10,0x100);
          iVar8 = iVar7 - iVar4 >> 8;
          if (0 < iVar7 - iVar4) {
            FUN_08056330(iVar11 + iVar8 * -0x100,iVar7 + iVar8 * -0x100);
          }
          FUN_08007160(iVar4,auStack_140,0x100);
        }
        else {
          FUN_08007160(auStack_140,iVar10,0x100);
          iVar6 = iVar10;
          while( true ) {
            iVar9 = iVar8;
            iVar8 = FUN_08056a38(auStack_140,iVar9,0x100);
            if (-1 < iVar8) break;
            FUN_08007160(iVar9 + 0x100,iVar9);
            iVar8 = iVar9 + -0x100;
            iVar6 = iVar9;
          }
          FUN_08007160(iVar6,auStack_140,0x100);
        }
        iVar11 = iVar11 + 0x100;
        iVar8 = iVar10;
      } while (iVar10 != DAT_0801f3d4);
      iVar4 = DAT_0801f3d4 + 0x100;
      if (iVar5 != iVar4) {
        iVar7 = DAT_0801f3d4;
        do {
          iVar11 = iVar7 + 0x100;
          FUN_08007160(auStack_140,iVar11,0x100);
          iVar8 = iVar11;
          while( true ) {
            iVar6 = iVar7;
            iVar7 = FUN_08056a38(auStack_140,iVar6,0x100);
            if (-1 < iVar7) break;
            FUN_08007160(iVar6 + 0x100,iVar6);
            iVar7 = iVar6 + -0x100;
            iVar8 = iVar6;
          }
          FUN_08007160(iVar8,auStack_140,0x100);
          iVar7 = iVar11;
        } while (iVar11 != iVar5 + (iVar10 - iVar4));
      }
    }
    iVar7 = *(int *)(iVar2 + 4);
  }
  FUN_0804cb68(DAT_0801f3d0,iVar7);
  return 0;
}


```

### callee `FUN_08056330` @ `08056330`
```c

void FUN_08056330(undefined *param_1,undefined *param_2,uint param_3)

{
  undefined *puVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  undefined *puVar4;
  int iVar5;
  uint uVar6;
  undefined4 *puVar7;
  
  if ((param_2 < param_1) && (puVar4 = param_2 + param_3, param_1 < puVar4)) {
    param_1 = param_1 + param_3;
    if (param_3 != 0) {
      do {
        puVar4 = puVar4 + -1;
        param_1 = param_1 + -1;
        *param_1 = *puVar4;
      } while (param_2 != puVar4);
      return;
    }
  }
  else {
    if (param_3 < 0x10) {
      if (param_3 == 0) {
        return;
      }
    }
    else if ((((uint)param_1 | (uint)param_2) & 3) == 0) {
      puVar1 = param_2 + 0x10;
      puVar4 = param_1 + 0x10;
      do {
        *(undefined4 *)(puVar4 + -0x10) = *(undefined4 *)(puVar1 + -0x10);
        *(undefined4 *)(puVar4 + -0xc) = *(undefined4 *)(puVar1 + -0xc);
        *(undefined4 *)(puVar4 + -8) = *(undefined4 *)(puVar1 + -8);
        *(undefined4 *)(puVar4 + -4) = *(undefined4 *)(puVar1 + -4);
        puVar1 = puVar1 + 0x10;
        puVar4 = puVar4 + 0x10;
      } while (puVar1 != param_2 + (param_3 - 0x10 & 0xfffffff0) + 0x20);
      iVar5 = (param_3 - 0x10 >> 4) + 1;
      puVar2 = (undefined4 *)(param_2 + iVar5 * 0x10);
      uVar6 = param_3 & 0xf;
      param_1 = param_1 + iVar5 * 0x10;
      if ((param_3 & 0xc) != 0) {
        puVar7 = (undefined4 *)(param_1 + -4);
        puVar3 = puVar2;
        do {
          puVar7 = puVar7 + 1;
          *puVar7 = *puVar3;
          puVar3 = puVar3 + 1;
        } while (puVar7 != (undefined4 *)(param_1 + (uVar6 - 4 & 0xfffffffc)));
        iVar5 = (uVar6 - 4 >> 2) + 1;
        uVar6 = param_3 & 3;
        param_1 = param_1 + iVar5 * 4;
        puVar2 = puVar2 + iVar5;
      }
      if (uVar6 != 0) {
        param_1 = param_1 + -1;
        puVar7 = puVar2;
        do {
          puVar3 = (undefined4 *)((int)puVar7 + 1);
          param_1 = param_1 + 1;
          *param_1 = *(undefined *)puVar7;
          puVar7 = puVar3;
        } while (puVar3 != (undefined4 *)(uVar6 + (int)puVar2));
      }
      return;
    }
    param_1 = param_1 + -1;
    puVar4 = param_2;
    do {
      puVar1 = puVar4 + 1;
      param_1 = param_1 + 1;
      *param_1 = *puVar4;
      puVar4 = puVar1;
    } while (puVar1 != param_2 + param_3);
  }
  return;
}


```

### callee `FUN_080523c0` @ `080523c0`
```c

uint FUN_080523c0(char **param_1,int param_2)

{
  int iVar1;
  uint uVar2;
  char *pcVar3;
  
  if (param_1 == (char **)0x0) {
    return 9;
  }
  pcVar3 = *param_1;
  if ((((pcVar3 == (char *)0x0) || (*pcVar3 == '\0')) ||
      (*(short *)(param_1 + 1) != *(short *)(pcVar3 + 6))) ||
     (iVar1 = FUN_08052c2c(pcVar3[1]), iVar1 << 0x1f < 0)) {
    return 9;
  }
  if (param_2 == 0) {
    uVar2 = FUN_0804f22c(param_1,0);
    return uVar2;
  }
  uVar2 = FUN_0804e924(param_1);
  if ((uVar2 & 0xfb) != 0) {
    return uVar2;
  }
  FUN_0804debc(param_1,param_2);
  uVar2 = FUN_0804e898(param_1);
  if (uVar2 == 4) {
    uVar2 = 0;
  }
  return uVar2;
}


```

### callee `FUN_0801ee50` @ `0801ee50`
```c

int FUN_0801ee50(char *param_1,undefined4 *param_2,int *param_3)

{
  bool bVar1;
  bool bVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  undefined4 *puVar9;
  int local_58;
  int local_54;
  undefined local_50;
  int local_4c;
  int local_48;
  int local_44;
  int iStack_40;
  int local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 uStack_30;
  undefined4 local_2c;
  
  if (*param_1 == '\0') {
    return 4;
  }
  FUN_0804cb68(DAT_0801f094,param_1);
  iVar6 = FUN_080510f0(DAT_0801f098,param_1,1);
  if (iVar6 == 0) {
    local_58 = iVar6;
    local_44 = iVar6;
    iStack_40 = iVar6;
    local_3c = iVar6;
    iVar7 = FUN_080513f8(DAT_0801f098,&local_44,0xc,&local_58);
    iVar5 = DAT_0801f0d0;
    iVar4 = DAT_0801f0cc;
    iVar6 = DAT_0801f0a8;
    if (iVar7 != 0) {
      FUN_0804cb58(DAT_0801f0c0);
      FUN_08051d88(DAT_0801f098);
      if (iVar7 == 1) {
LAB_0801f028:
        *DAT_0801f0a0 = 3;
        return 1;
      }
      if (iVar7 != 0x12) {
        *DAT_0801f0a0 = 0;
        return iVar7;
      }
LAB_0801f01e:
      *DAT_0801f0a0 = 2;
      return 0x12;
    }
    if ((local_44 == DAT_0801f0a4) && (local_3c == DAT_0801f0a4 + -0xf007fb)) {
      iVar7 = DAT_0801f0a8 + 0x46c;
      bVar1 = false;
      bVar2 = false;
      local_4c = 0;
      local_48 = 0;
      local_38 = 0;
      local_34 = 0;
      uStack_30 = 0;
      local_2c = 0;
      do {
        while( true ) {
          while( true ) {
            if (*(int *)(iVar6 + 0x484) == *(int *)(iVar6 + 0x478)) {
              if ((!bVar1) || (!bVar2)) goto LAB_0801ef48;
              goto LAB_0801ef40;
            }
            iVar8 = FUN_080513f8(iVar7,&local_4c,8,&local_58);
            if (iVar8 != 0) {
              FUN_0804cb58(DAT_0801f0c0);
              FUN_08051d88(DAT_0801f098);
              if (iVar8 == 1) goto LAB_0801f028;
              if (iVar8 != 0x12) {
                *DAT_0801f0a0 = 0;
                return iVar8;
              }
              goto LAB_0801f01e;
            }
            if (local_4c != iVar4) break;
            iVar8 = FUN_080513f8(iVar7,&local_38,0x10,&local_58);
            if (iVar8 != 0) {
              FUN_0804cb68(DAT_0801f0c0);
              FUN_08051d88(DAT_0801f098);
              if (iVar8 != 1) {
                FUN_0801d860(iVar8);
                return iVar8;
              }
              goto LAB_0801f028;
            }
            if (((((local_38 & 0xffff) != 1) && ((local_38 & 0xffff) != 0xfffe)) ||
                (local_38._2_2_ != 2)) || (local_2c._2_2_ != 0x10)) {
              FUN_0804cb68(DAT_0801f0c4);
              goto LAB_0801ef6a;
            }
            FUN_0804cb58(DAT_0801f0bc);
            if (bVar1) goto LAB_0801ef40;
            FUN_08051f1c(iVar7,*(int *)(iVar6 + 0x484) + local_48 + -0x10);
            bVar2 = true;
          }
          if (local_4c != iVar5) break;
          *param_2 = *(undefined4 *)(iVar6 + 0x484);
          uVar3 = DAT_0801f0b8;
          *param_3 = local_48;
          FUN_0804cb68(uVar3);
          if (bVar2) goto LAB_0801ef40;
          bVar1 = true;
          FUN_08051f1c(iVar7,*(int *)(iVar6 + 0x484) + local_48);
        }
        local_50 = 0;
        local_54 = local_4c;
        FUN_0804cb68(DAT_0801f0ac,&local_54);
        FUN_08051f1c(iVar7,*(int *)(iVar6 + 0x484) + local_48);
      } while ((!bVar1) || (!bVar2));
LAB_0801ef40:
      if (*param_3 == 0) {
LAB_0801ef48:
        iVar6 = 0x13;
        FUN_0804cb58(DAT_0801f0b0);
      }
      else {
        FUN_0804cb58(DAT_0801f0c8);
        iVar6 = 0;
      }
      FUN_08051d88(DAT_0801f098);
      return iVar6;
    }
    FUN_0804cb58(DAT_0801f0b4);
LAB_0801ef6a:
    puVar9 = DAT_0801f0a0;
    iVar6 = 0x13;
    FUN_08051d88(DAT_0801f098);
  }
  else {
    FUN_0804cb58(DAT_0801f09c);
    FUN_08051d88(DAT_0801f098);
    if (iVar6 == 1) {
      *DAT_0801f0a0 = 3;
      return 1;
    }
    puVar9 = DAT_0801f0a0;
    if (iVar6 == 0x12) {
      *DAT_0801f0a0 = 2;
      return 0x12;
    }
  }
  *puVar9 = 0;
  return iVar6;
}


```

### callee `FUN_08056b1c` @ `08056b1c`
```c

int FUN_08056b1c(int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  
  if (param_2 != 0) {
    iVar2 = 0;
    while (iVar1 = FUN_0805a59c(param_1,param_2,param_3,param_1,param_4), iVar1 != 0) {
      param_1 = iVar1 + 1;
      iVar2 = iVar1;
    }
    return iVar2;
  }
  iVar2 = FUN_0805a59c();
  return iVar2;
}


```

### callee `FUN_080522b8` @ `080522b8`
```c

int FUN_080522b8(char **param_1,undefined4 param_2)

{
  ushort uVar1;
  int iVar2;
  char *pcVar3;
  undefined4 local_1c [2];
  char *local_14 [2];
  
  if (param_1 == (char **)0x0) {
    return 9;
  }
  local_1c[0] = param_2;
  iVar2 = FUN_0804e3ac(local_1c,local_14,0);
  if (iVar2 != 0) goto LAB_080522d2;
  *param_1 = local_14[0];
  iVar2 = FUN_0804fc10(param_1,local_1c[0]);
  if (iVar2 == 0) {
    if (*(char *)((int)param_1 + 0x2f) < '\0') {
LAB_0805230e:
      *(undefined2 *)(param_1 + 1) = *(undefined2 *)(local_14[0] + 6);
      iVar2 = FUN_0804f22c(param_1,0);
      if (iVar2 == 0) {
        if (param_1[2] == (char *)0x0) {
          param_1[4] = (char *)0x0;
          return 0;
        }
        pcVar3 = (char *)FUN_0804de14(param_1,0);
        param_1[4] = pcVar3;
        if (pcVar3 != (char *)0x0) {
          return 0;
        }
        iVar2 = 0x12;
        goto LAB_080522d2;
      }
      goto LAB_08052326;
    }
    if ((int)((uint)*(byte *)((int)param_1 + 6) << 0x1b) < 0) {
      uVar1 = *(ushort *)(param_1[8] + 0x1a);
      pcVar3 = (char *)(uint)uVar1;
      if (*local_14[0] == '\x03') {
        pcVar3 = (char *)CONCAT22(*(undefined2 *)(param_1[8] + 0x14),uVar1);
      }
      param_1[2] = pcVar3;
      goto LAB_0805230e;
    }
  }
  else {
LAB_08052326:
    if (iVar2 != 4) goto LAB_080522d2;
  }
  iVar2 = 5;
LAB_080522d2:
  *param_1 = (char *)0x0;
  return iVar2;
}


```

### callee `FUN_0801dd9c` @ `0801dd9c`
```c

void FUN_0801dd9c(int param_1,uint param_2,int param_3)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  undefined auStack_120 [256];
  
  iVar1 = param_2 - param_1;
  if (iVar1 < 0x1001) {
    return;
  }
  if (param_3 == 0) {
LAB_0801de9a:
    FUN_0801d9f0(param_1,param_2);
    iVar1 = param_2 - 0x100;
    FUN_0801d874(param_1,iVar1,iVar1);
    uVar5 = ((param_2 - param_1) + -0x101) * 0x200000 >> 0x1d;
    if (0x100 < iVar1 - param_1) {
      if (uVar5 != 0) {
        if (uVar5 != 1) {
          if (uVar5 != 2) {
            if (uVar5 != 3) {
              if (uVar5 != 4) {
                if (uVar5 != 5) {
                  if (uVar5 != 6) {
                    iVar1 = param_2 - 0x200;
                    FUN_0801d874(param_1,iVar1,iVar1);
                  }
                  iVar1 = iVar1 + -0x100;
                  FUN_0801d874(param_1,iVar1,iVar1);
                }
                iVar1 = iVar1 + -0x100;
                FUN_0801d874(param_1,iVar1,iVar1);
              }
              iVar1 = iVar1 + -0x100;
              FUN_0801d874(param_1,iVar1,iVar1);
            }
            iVar1 = iVar1 + -0x100;
            FUN_0801d874(param_1,iVar1,iVar1);
          }
          iVar1 = iVar1 + -0x100;
          FUN_0801d874(param_1,iVar1,iVar1);
        }
        iVar1 = iVar1 + -0x100;
        FUN_0801d874(param_1,iVar1,iVar1);
        if (iVar1 - param_1 < 0x101) {
          return;
        }
      }
      do {
        FUN_0801d874(param_1,iVar1 + -0x100,iVar1 + -0x100);
        FUN_0801d874(param_1,iVar1 + -0x200);
        FUN_0801d874(param_1,iVar1 + -0x300);
        FUN_0801d874(param_1,iVar1 + -0x400);
        FUN_0801d874(param_1,iVar1 + -0x500);
        FUN_0801d874(param_1,iVar1 + -0x600);
        iVar2 = iVar1 + -0x700;
        iVar1 = iVar1 + -0x800;
        FUN_0801d874(param_1,iVar2);
        FUN_0801d874(param_1,iVar1,iVar1);
      } while (0x100 < iVar1 - param_1);
    }
    return;
  }
  uVar6 = param_1 + 0x100;
  uVar5 = param_2;
LAB_0801ddba:
  param_3 = param_3 + -1;
  iVar2 = param_1 + (iVar1 >> 9) * 0x100;
  iVar4 = uVar5 - 0x100;
  iVar1 = FUN_08056a38(uVar6,iVar2,0x100);
  uVar3 = uVar5;
  param_2 = uVar6;
  if (iVar1 < 0) {
    iVar1 = FUN_08056a38(iVar2,iVar4,0x100);
    if (-1 < iVar1) {
      iVar1 = FUN_08056a38(uVar6,iVar4);
      if (iVar1 < 0) goto LAB_0801dfee;
      goto LAB_0801dfc8;
    }
    FUN_08007160(auStack_120,param_1,0x100);
  }
  else {
    iVar1 = FUN_08056a38(uVar6,iVar4,0x100);
    if (iVar1 < 0) {
LAB_0801dfc8:
      FUN_08007160(auStack_120,param_1,0x100);
      FUN_08007160(param_1,uVar6,0x100);
      FUN_08007160(uVar6,auStack_120,0x100);
      goto LAB_0801de26;
    }
    iVar1 = FUN_08056a38(iVar2,iVar4,0x100);
    if (iVar1 < 0) {
LAB_0801dfee:
      FUN_08007160(auStack_120,param_1,0x100);
      FUN_08007160(param_1,iVar4,0x100);
      FUN_08007160(iVar4,auStack_120,0x100);
      goto LAB_0801de26;
    }
    FUN_08007160(auStack_120,param_1,0x100);
  }
  FUN_08007160(param_1,iVar2,0x100);
  FUN_08007160(iVar2,auStack_120,0x100);
LAB_0801de26:
  do {
    iVar1 = FUN_08056a38(param_2,param_1,0x100);
    if (-1 < iVar1) {
      do {
        uVar3 = uVar3 - 0x100;
        iVar1 = FUN_08056a38(param_1,uVar3,0x100);
      } while (iVar1 < 0);
      if (uVar3 <= param_2) break;
      FUN_08007160(auStack_120,param_2,0x100);
      FUN_08007160(param_2,uVar3,0x100);
      FUN_08007160(uVar3,auStack_120,0x100);
    }
    param_2 = param_2 + 0x100;
  } while( true );
  FUN_0801dd9c(param_2,uVar5,param_3);
  iVar1 = param_2 - param_1;
  if (iVar1 < 0x1001) {
    return;
  }
  uVar5 = param_2;
  if (param_3 == 0) goto LAB_0801de9a;
  goto LAB_0801ddba;
}


```

### callee `FUN_0805234c` @ `0805234c`
```c

undefined4 FUN_0805234c(char **param_1)

{
  short sVar1;
  int iVar2;
  uint uVar3;
  char *pcVar4;
  int iVar5;
  
  if (param_1 == (char **)0x0) {
    return 9;
  }
  pcVar4 = *param_1;
  if ((((pcVar4 == (char *)0x0) || (*pcVar4 == '\0')) ||
      (*(short *)(param_1 + 1) != *(short *)(pcVar4 + 6))) ||
     (uVar3 = FUN_08052c2c(pcVar4[1]), iVar2 = DAT_080523bc, (uVar3 & 1) != 0)) {
    return 9;
  }
  if (param_1[4] != (char *)0x0) {
    pcVar4 = param_1[4] + -1;
    if (&UNK_00000001 < pcVar4) {
      return 2;
    }
    iVar5 = DAT_080523bc + (int)pcVar4 * 0x10;
    sVar1 = *(short *)(iVar5 + 0xc);
    if (sVar1 == 0x100) {
      *(undefined2 *)(iVar5 + 0xc) = 0;
    }
    else if ((sVar1 != 0) && (*(short *)(iVar5 + 0xc) = sVar1 + -1, sVar1 != 1)) goto LAB_08052398;
    *(undefined4 *)(iVar2 + (int)pcVar4 * 0x10) = 0;
  }
LAB_08052398:
  *param_1 = (char *)0x0;
  return 0;
}


```

---
## `FUN_0801facc`  @ `0801facc`
- **Anchors:** /Multigrain/Wavs
- **Strings seen:** /Multigrain/Wavs
- **Signature:** `undefined FUN_0801facc()`
- **Params:** 0  **Calls:** 10 funcs

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

### callee `FUN_0801ebf4` @ `0801ebf4`
```c

int FUN_0801ebf4(void)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  undefined auStack_16c [52];
  undefined auStack_138 [8];
  byte local_130;
  short local_122;
  short local_120;
  short local_11e;
  char local_11c;
  undefined auStack_11b [255];
  
  FUN_0804cb58(DAT_0801ee34);
  uVar3 = DAT_0801ee40;
  uVar2 = DAT_0801ee3c;
  puVar1 = DAT_0801ee38;
  *DAT_0801ee38 = 0;
  puVar1[1] = 0;
  FUN_08051058(uVar3,uVar2,1);
  iVar4 = FUN_080522b8(auStack_16c,DAT_0801ee44);
  uVar3 = DAT_0801ee4c;
  uVar2 = DAT_0801ee44;
  if (iVar4 == 0) {
    iVar7 = 100;
    iVar8 = 0;
    while ((iVar5 = FUN_080523c0(auStack_16c,auStack_138), iVar5 == 0 && ((char)local_122 != '\0')))
    {
      if (((int)((uint)local_130 << 0x1b) < 0) &&
         ((((local_122 == 0x7250 && (local_120 == 0x6a6f)) && (local_11e == 0x6365)) &&
          (local_11c == 't')))) {
        iVar5 = FUN_08055818(auStack_11b);
        uVar6 = iVar5 - 1;
        if (uVar6 < 0x30) {
          iVar8 = iVar8 + 1;
          puVar1[uVar6 >> 5] = 1 << (uVar6 & 0x1f) | puVar1[uVar6 >> 5];
          FUN_0804cb68(uVar3,uVar2,&local_122);
        }
      }
      iVar5 = FUN_080523c0(auStack_16c,auStack_138);
      if ((iVar5 != 0) || ((char)local_122 == '\0')) break;
      if (((((int)((uint)local_130 << 0x1b) < 0) && ((local_122 == 0x7250 && (local_120 == 0x6a6f)))
           ) && (local_11e == 0x6365)) && (local_11c == 't')) {
        iVar5 = FUN_08055818(auStack_11b);
        uVar6 = iVar5 - 1;
        if (uVar6 < 0x30) {
          iVar8 = iVar8 + 1;
          puVar1[uVar6 >> 5] = 1 << (uVar6 & 0x1f) | puVar1[uVar6 >> 5];
          FUN_0804cb68(uVar3,uVar2,&local_122);
        }
      }
      iVar5 = FUN_080523c0(auStack_16c,auStack_138);
      if ((iVar5 != 0) || ((char)local_122 == '\0')) break;
      if ((((int)((uint)local_130 << 0x1b) < 0) &&
          (((local_122 == 0x7250 && (local_120 == 0x6a6f)) && (local_11e == 0x6365)))) &&
         (local_11c == 't')) {
        iVar5 = FUN_08055818(auStack_11b);
        uVar6 = iVar5 - 1;
        if (uVar6 < 0x30) {
          iVar8 = iVar8 + 1;
          puVar1[uVar6 >> 5] = 1 << (uVar6 & 0x1f) | puVar1[uVar6 >> 5];
          FUN_0804cb68(uVar3,uVar2,&local_122);
        }
      }
      iVar5 = FUN_080523c0(auStack_16c,auStack_138);
      if ((iVar5 != 0) || ((char)local_122 == '\0')) break;
      if (((int)((uint)local_130 << 0x1b) < 0) && ((local_122 == 0x7250 && (local_120 == 0x6a6f))))
      {
        if ((local_11e == 0x6365) && (local_11c == 't')) {
          iVar5 = FUN_08055818(auStack_11b);
          uVar6 = iVar5 - 1;
          if (uVar6 < 0x30) {
            iVar8 = iVar8 + 1;
            puVar1[uVar6 >> 5] = 1 << (uVar6 & 0x1f) | puVar1[uVar6 >> 5];
            FUN_0804cb68(uVar3,uVar2,&local_122);
          }
        }
      }
      iVar7 = iVar7 + -4;
      if (iVar7 == 0) break;
    }
    FUN_0805234c(auStack_16c);
    FUN_0804cb68(DAT_0801ee48,iVar8);
  }
  return iVar4;
}


```

### callee `FUN_0805253c` @ `0805253c`
```c

int FUN_0805253c(undefined4 param_1)

{
  char cVar1;
  char cVar2;
  char *pcVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  uint uVar8;
  int iVar9;
  byte bVar10;
  char *pcVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  char *pcVar15;
  int iVar16;
  char cVar17;
  bool bVar18;
  undefined4 local_64;
  char *local_60;
  char *local_5c [2];
  int local_54;
  int local_50;
  int local_3c;
  byte local_2d;
  char cVar3;
  
  local_64 = param_1;
  iVar5 = FUN_0804e3ac(&local_64,&local_60,2);
  local_5c[0] = local_60;
  if (iVar5 != 0) {
    return iVar5;
  }
  iVar5 = FUN_0804fc10(local_5c,local_64);
  if (iVar5 == 0) {
    return 8;
  }
  if (iVar5 != 4) {
    return iVar5;
  }
  bVar10 = local_2d & 0x20;
  if ((local_2d & 0x20) != 0) {
    return 6;
  }
  iVar5 = FUN_0804f088(local_5c,bVar10);
  pcVar4 = local_60;
  local_50 = (uint)*(ushort *)(local_60 + 10) << 9;
  if (iVar5 == 0) {
    iVar9 = 7;
  }
  else {
    if (iVar5 != 1) {
      if (iVar5 == -1) {
LAB_080528b0:
        iVar9 = 1;
        FUN_0801fefc();
      }
      else {
        if (local_60[3] != '\0') {
          iVar16 = *(int *)(local_60 + 0x34);
          pcVar15 = local_60 + 0x38;
          iVar9 = FUN_08052c80(local_60[1],pcVar15,iVar16,1);
          if (iVar9 != 0) goto LAB_080528b0;
          uVar6 = *(uint *)(pcVar4 + 0x20);
          pcVar4[3] = bVar10;
          if (((uint)(iVar16 - *(int *)(pcVar4 + 0x28)) < uVar6) &&
             (uVar8 = (uint)(byte)pcVar4[2], 1 < uVar8)) {
            uVar13 = uVar8 - 2 & 7;
            uVar12 = uVar8;
            if (uVar13 != 0) {
              iVar16 = iVar16 + uVar6;
              uVar12 = uVar8 - 1;
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              uVar6 = *(uint *)(pcVar4 + 0x20);
              if (uVar13 != 1) {
                if (uVar13 != 2) {
                  if (uVar13 != 3) {
                    if (uVar13 != 4) {
                      if (uVar13 != 5) {
                        if (uVar13 != 6) {
                          iVar16 = iVar16 + uVar6;
                          uVar12 = uVar8 - 2;
                          FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                          uVar6 = *(uint *)(pcVar4 + 0x20);
                        }
                        iVar16 = iVar16 + uVar6;
                        uVar12 = uVar12 - 1;
                        FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                        uVar6 = *(uint *)(pcVar4 + 0x20);
                      }
                      iVar16 = iVar16 + uVar6;
                      uVar12 = uVar12 - 1;
                      FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                      uVar6 = *(uint *)(pcVar4 + 0x20);
                    }
                    iVar16 = iVar16 + uVar6;
                    uVar12 = uVar12 - 1;
                    FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                    uVar6 = *(uint *)(pcVar4 + 0x20);
                  }
                  iVar16 = iVar16 + uVar6;
                  uVar12 = uVar12 - 1;
                  FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                  uVar6 = *(uint *)(pcVar4 + 0x20);
                }
                iVar16 = iVar16 + uVar6;
                uVar12 = uVar12 - 1;
                FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
                uVar6 = *(uint *)(pcVar4 + 0x20);
              }
            }
            while( true ) {
              FUN_08052c80(pcVar4[1],pcVar15,iVar16 + uVar6,1);
              bVar18 = uVar12 == 2;
              uVar12 = uVar12 - 8;
              if (bVar18) break;
              iVar16 = iVar16 + uVar6 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              iVar16 = iVar16 + *(int *)(pcVar4 + 0x20);
              FUN_08052c80(pcVar4[1],pcVar15,iVar16,1);
              uVar6 = *(uint *)(pcVar4 + 0x20);
            }
          }
        }
        uVar6 = FUN_0801fefc();
        pcVar4 = local_60;
        if (iVar5 - 2U < *(int *)(local_60 + 0x1c) - 2U) {
          iVar9 = (iVar5 - 2U) * (uint)*(ushort *)(local_60 + 10) + *(int *)(local_60 + 0x30);
        }
        else {
          iVar9 = 0;
        }
        pcVar15 = local_60 + 0x38;
        FUN_08056428(pcVar15,0,0x200);
        *(undefined4 *)(pcVar4 + 0x38) = 0x20202020;
        *(undefined4 *)(pcVar4 + 0x3c) = 0x20202020;
        *(undefined4 *)(pcVar4 + 0x3f) = 0x20202020;
        pcVar4[0x4f] = (char)(uVar6 >> 8);
        pcVar4[0x4e] = (char)uVar6;
        pcVar4[0x38] = '.';
        pcVar4[0x43] = '\x10';
        pcVar4[0x50] = (char)(uVar6 >> 0x10);
        pcVar4[0x51] = (char)(uVar6 >> 0x18);
        pcVar4[0x52] = (char)iVar5;
        cVar1 = (char)((uint)iVar5 >> 8);
        pcVar4[0x53] = cVar1;
        cVar2 = (char)((uint)iVar5 >> 0x10);
        cVar3 = (char)((uint)iVar5 >> 0x18);
        if (*pcVar4 == '\x03') {
          pcVar4[0x4c] = cVar2;
          pcVar4[0x4d] = cVar3;
        }
        *(undefined4 *)(pcVar4 + 0x58) = *(undefined4 *)(pcVar4 + 0x38);
        *(undefined4 *)(pcVar4 + 0x5c) = *(undefined4 *)(pcVar4 + 0x3c);
        *(undefined4 *)(pcVar4 + 0x60) = *(undefined4 *)(pcVar4 + 0x40);
        *(undefined4 *)(pcVar4 + 100) = *(undefined4 *)(pcVar4 + 0x44);
        *(undefined4 *)(pcVar4 + 0x68) = *(undefined4 *)(pcVar4 + 0x48);
        *(undefined4 *)(pcVar4 + 0x74) = *(undefined4 *)(pcVar4 + 0x54);
        *(undefined4 *)(pcVar4 + 0x6c) = *(undefined4 *)(pcVar4 + 0x4c);
        *(undefined4 *)(pcVar4 + 0x70) = *(undefined4 *)(pcVar4 + 0x50);
        pcVar4[0x59] = '.';
        if ((*local_60 == '\x03') && (*(int *)(local_60 + 0x2c) == local_54)) {
          cVar17 = '\0';
          local_54 = 0;
        }
        else {
          bVar10 = (byte)local_54;
          cVar17 = (char)((uint)local_54 >> 8);
        }
        pcVar4[0x72] = bVar10;
        pcVar4[0x73] = cVar17;
        if (*local_60 == '\x03') {
          pcVar4[0x6c] = (char)((uint)local_54 >> 0x10);
          pcVar4[0x6d] = (char)((uint)local_54 >> 0x18);
        }
        if (*(ushort *)(local_60 + 10) == 0) {
LAB_0805285c:
          iVar9 = FUN_08050238(local_5c);
          if (iVar9 == 0) {
            *(char *)(local_3c + 0x1b) = cVar1;
            *(uint *)(local_3c + 0x16) =
                 uVar6 & 0xff | ((uVar6 << 0x10) >> 0x18) << 8 | ((uVar6 << 8) >> 0x18) << 0x10 |
                 uVar6 & 0xff000000;
            *(char *)(local_3c + 0x1a) = (char)iVar5;
            if (*local_60 == '\x03') {
              *(char *)(local_3c + 0x14) = cVar2;
              *(char *)(local_3c + 0x15) = cVar3;
            }
            *(undefined *)(local_3c + 0xb) = 0x10;
            local_60[3] = '\x01';
            iVar5 = FUN_0804ee7c();
            return iVar5;
          }
        }
        else {
          iVar16 = (*(ushort *)(local_60 + 10) - 1) + iVar9;
          while( true ) {
            pcVar4 = local_60;
            pcVar11 = local_60 + 0x38;
            local_60[3] = '\x01';
            *(int *)(local_60 + 0x34) = iVar9;
            iVar7 = FUN_08052c80(local_60[1],pcVar11,iVar9,1);
            if (iVar7 != 0) break;
            uVar8 = *(uint *)(pcVar4 + 0x20);
            pcVar4[3] = '\0';
            if (((uint)(iVar9 - *(int *)(pcVar4 + 0x28)) < uVar8) &&
               (uVar12 = (uint)(byte)pcVar4[2], 1 < uVar12)) {
              uVar14 = uVar12 - 2 & 7;
              uVar13 = uVar12;
              iVar7 = iVar9;
              if (uVar14 != 0) {
                iVar7 = iVar9 + uVar8;
                uVar13 = uVar12 - 1;
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                uVar8 = *(uint *)(pcVar4 + 0x20);
                if (uVar14 != 1) {
                  if (uVar14 != 2) {
                    if (uVar14 != 3) {
                      if (uVar14 != 4) {
                        if (uVar14 != 5) {
                          if (uVar14 != 6) {
                            iVar7 = iVar7 + uVar8;
                            uVar13 = uVar12 - 2;
                            FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                            uVar8 = *(uint *)(pcVar4 + 0x20);
                          }
                          iVar7 = iVar7 + uVar8;
                          uVar13 = uVar13 - 1;
                          FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                          uVar8 = *(uint *)(pcVar4 + 0x20);
                        }
                        iVar7 = iVar7 + uVar8;
                        uVar13 = uVar13 - 1;
                        FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                        uVar8 = *(uint *)(pcVar4 + 0x20);
                      }
                      iVar7 = iVar7 + uVar8;
                      uVar13 = uVar13 - 1;
                      FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                      uVar8 = *(uint *)(pcVar4 + 0x20);
                    }
                    iVar7 = iVar7 + uVar8;
                    uVar13 = uVar13 - 1;
                    FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                    uVar8 = *(uint *)(pcVar4 + 0x20);
                  }
                  iVar7 = iVar7 + uVar8;
                  uVar13 = uVar13 - 1;
                  FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                  uVar8 = *(uint *)(pcVar4 + 0x20);
                }
              }
              while( true ) {
                FUN_08052c80(pcVar4[1],pcVar11,iVar7 + uVar8,1);
                bVar18 = uVar13 == 2;
                uVar13 = uVar13 - 8;
                if (bVar18) break;
                iVar7 = iVar7 + uVar8 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                iVar7 = iVar7 + *(int *)(pcVar4 + 0x20);
                FUN_08052c80(pcVar4[1],pcVar11,iVar7,1);
                uVar8 = *(uint *)(pcVar4 + 0x20);
              }
            }
            FUN_08056428(pcVar15,0,0x200);
            if (iVar16 == iVar9) goto LAB_0805285c;
            iVar9 = iVar9 + 1;
          }
          iVar9 = 1;
        }
      }
      goto LAB_08052840;
    }
    iVar9 = 2;
  }
  FUN_0801fefc();
LAB_08052840:
  FUN_08050100(local_5c,iVar5,0);
  return iVar9;
}


```

### callee `FUN_08052a94` @ `08052a94`
```c

undefined4 FUN_08052a94(undefined4 param_1,char *param_2)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  int iVar4;
  
  iVar4 = DAT_08052ae0;
  if (*(char *)(DAT_08052ae0 + 9) == '\0') {
    bVar1 = *(byte *)(DAT_08052ae0 + 9);
    *(undefined *)(DAT_08052ae0 + (uint)*(byte *)(DAT_08052ae0 + 9)) = 0;
    bVar2 = *(byte *)(iVar4 + 9);
    *(undefined4 *)(iVar4 + (uint)bVar1 * 4 + 4) = param_1;
    cVar3 = *(char *)(iVar4 + 9);
    *(undefined *)((uint)bVar2 + iVar4 + 8) = 0;
    *(char *)(iVar4 + 9) = cVar3 + '\x01';
    *param_2 = cVar3 + '0';
    param_2[1] = ':';
    param_2[3] = '\0';
    param_2[2] = '/';
    return 0;
  }
  return 1;
}


```

### callee `FUN_0801f0d4` @ `0801f0d4`
```c

int FUN_0801f0d4(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  int iVar10;
  int iVar11;
  undefined auStack_17c [4];
  undefined auStack_178 [4];
  undefined auStack_174 [52];
  undefined auStack_140 [8];
  byte local_138;
  undefined auStack_137 [13];
  char local_12a [262];
  
  FUN_0804cb58(DAT_0801f3b4);
  FUN_08051058(DAT_0801f3bc,DAT_0801f3b8,1);
  iVar4 = FUN_080522b8(auStack_174,DAT_0801f3c0);
  if ((iVar4 != 0) ||
     (iVar4 = FUN_08051eb0(DAT_0801f3c0), iVar7 = DAT_0801f3cc, uVar3 = DAT_0801f3c8,
     iVar2 = DAT_0801f3c4, uVar1 = DAT_0801f3c0, iVar4 != 0)) {
    return iVar4;
  }
  iVar4 = 0x400;
  *(undefined4 *)(DAT_0801f3c4 + 4) = 0;
  while ((iVar5 = FUN_080523c0(auStack_174,auStack_140), iVar5 == 0 && (local_12a[0] != '\0'))) {
    if ((-1 < (int)((uint)local_138 << 0x1e)) &&
       ((((local_12a[0] != '.' && (iVar5 = FUN_08056b1c(auStack_137,0x2e), iVar5 != 0)) &&
         (*(char *)(iVar5 + 1) == 'W')) &&
        ((*(char *)(iVar5 + 2) == 'A' && (*(char *)(iVar5 + 3) == 'V')))))) {
      iVar5 = FUN_0801ee50(local_12a,auStack_17c,auStack_178);
      if (iVar5 == 0) {
        iVar5 = iVar7 + *(int *)(iVar2 + 4) * 0x100;
        *(int *)(iVar2 + 4) = *(int *)(iVar2 + 4) + 1;
        FUN_08056ab8(iVar5,local_12a,0x100);
        *(undefined *)(iVar5 + 0xff) = 0;
        FUN_0804cb68(uVar3,uVar1,local_12a);
      }
      if (*(int *)(iVar2 + 4) == 0x80) break;
    }
    iVar5 = FUN_080523c0(auStack_174,auStack_140);
    if ((iVar5 != 0) || (local_12a[0] == '\0')) break;
    if (((-1 < (int)((uint)local_138 << 0x1e)) &&
        (((local_12a[0] != '.' && (iVar5 = FUN_08056b1c(auStack_137,0x2e), iVar5 != 0)) &&
         (*(char *)(iVar5 + 1) == 'W')))) &&
       ((*(char *)(iVar5 + 2) == 'A' && (*(char *)(iVar5 + 3) == 'V')))) {
      iVar5 = FUN_0801ee50(local_12a,auStack_17c,auStack_178);
      if (iVar5 == 0) {
        iVar5 = iVar7 + *(int *)(iVar2 + 4) * 0x100;
        *(int *)(iVar2 + 4) = *(int *)(iVar2 + 4) + 1;
        FUN_08056ab8(iVar5,local_12a,0x100);
        *(undefined *)(iVar5 + 0xff) = 0;
        FUN_0804cb68(uVar3,uVar1,local_12a);
      }
      if (*(int *)(iVar2 + 4) == 0x80) break;
    }
    iVar4 = iVar4 + -2;
    if (iVar4 == 0) break;
  }
  FUN_0805234c(auStack_174);
  iVar4 = DAT_0801f3cc;
  iVar7 = *(int *)(iVar2 + 4);
  if ((iVar7 != 0) && (iVar5 = DAT_0801f3cc + iVar7 * 0x100, iVar5 != DAT_0801f3cc)) {
    iVar7 = iVar5 - DAT_0801f3cc;
    FUN_0801dd9c(DAT_0801f3cc,iVar5,(0x1f - LZCOUNT(iVar7 >> 8)) * 2);
    if (iVar7 < 0x1001) {
      iVar8 = iVar4 + 0x100;
      iVar7 = iVar4;
      while (iVar5 != iVar8) {
        iVar11 = iVar7 + 0x100;
        iVar8 = FUN_08056a38(iVar11,iVar4,0x100);
        if (iVar8 < 0) {
          FUN_08007160(auStack_140,iVar11,0x100);
          iVar8 = iVar11 - iVar4 >> 8;
          if (0 < iVar11 - iVar4) {
            FUN_08056330(iVar7 + 0x200 + iVar8 * -0x100,iVar11 + iVar8 * -0x100);
          }
          FUN_08007160(iVar4,auStack_140,0x100);
        }
        else {
          FUN_08007160(auStack_140,iVar7 + 0x100,0x100);
          iVar8 = iVar7;
          iVar6 = iVar7 + 0x100;
          while( true ) {
            iVar10 = iVar8;
            iVar8 = FUN_08056a38(auStack_140,iVar10,0x100);
            if (-1 < iVar8) break;
            FUN_08007160(iVar10 + 0x100,iVar10);
            iVar8 = iVar10 + -0x100;
            iVar6 = iVar10;
          }
          FUN_08007160(iVar6,auStack_140,0x100);
        }
        iVar8 = iVar7 + 0x200;
        iVar7 = iVar11;
      }
    }
    else {
      iVar11 = iVar4 + 0x200;
      iVar8 = iVar4;
      iVar7 = iVar4;
      do {
        iVar7 = iVar7 + 0x100;
        iVar10 = iVar8 + 0x100;
        iVar6 = FUN_08056a38(iVar7,iVar4,0x100);
        if (iVar6 < 0) {
          FUN_08007160(auStack_140,iVar10,0x100);
          iVar8 = iVar7 - iVar4 >> 8;
          if (0 < iVar7 - iVar4) {
            FUN_08056330(iVar11 + iVar8 * -0x100,iVar7 + iVar8 * -0x100);
          }
          FUN_08007160(iVar4,auStack_140,0x100);
        }
        else {
          FUN_08007160(auStack_140,iVar10,0x100);
          iVar6 = iVar10;
          while( true ) {
            iVar9 = iVar8;
            iVar8 = FUN_08056a38(auStack_140,iVar9,0x100);
            if (-1 < iVar8) break;
            FUN_08007160(iVar9 + 0x100,iVar9);
            iVar8 = iVar9 + -0x100;
            iVar6 = iVar9;
          }
          FUN_08007160(iVar6,auStack_140,0x100);
        }
        iVar11 = iVar11 + 0x100;
        iVar8 = iVar10;
      } while (iVar10 != DAT_0801f3d4);
      iVar4 = DAT_0801f3d4 + 0x100;
      if (iVar5 != iVar4) {
        iVar7 = DAT_0801f3d4;
        do {
          iVar11 = iVar7 + 0x100;
          FUN_08007160(auStack_140,iVar11,0x100);
          iVar8 = iVar11;
          while( true ) {
            iVar6 = iVar7;
            iVar7 = FUN_08056a38(auStack_140,iVar6,0x100);
            if (-1 < iVar7) break;
            FUN_08007160(iVar6 + 0x100,iVar6);
            iVar7 = iVar6 + -0x100;
            iVar8 = iVar6;
          }
          FUN_08007160(iVar8,auStack_140,0x100);
          iVar7 = iVar11;
        } while (iVar11 != iVar5 + (iVar10 - iVar4));
      }
    }
    iVar7 = *(int *)(iVar2 + 4);
  }
  FUN_0804cb68(DAT_0801f3d0,iVar7);
  return 0;
}


```

### callee `FUN_0801f848` @ `0801f848`
```c

int FUN_0801f848(void)

{
  int *piVar1;
  undefined4 uVar2;
  int iVar3;
  uint uVar4;
  undefined4 uVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int *piVar9;
  int *piVar10;
  int *piVar11;
  int *piVar12;
  int *piVar13;
  undefined auStack_174 [4];
  undefined auStack_170 [4];
  undefined auStack_16c [52];
  undefined auStack_138 [8];
  undefined4 local_130;
  undefined auStack_12c [10];
  char local_122 [258];
  
  FUN_0804cb58(DAT_0801faa4);
  FUN_08051058(DAT_0801faac,DAT_0801faa8,1);
  iVar6 = FUN_080522b8(auStack_16c,DAT_0801fab0);
  if ((iVar6 != 0) ||
     (iVar6 = FUN_08051eb0(DAT_0801fab0), piVar9 = DAT_0801fabc, uVar4 = DAT_0801fab8,
     iVar3 = DAT_0801fab4, uVar2 = DAT_0801fab0, iVar6 != 0)) {
    return iVar6;
  }
  iVar6 = 0x400;
  *(undefined4 *)(DAT_0801fab4 + 8) = 0;
  while ((iVar7 = FUN_080523c0(auStack_16c,auStack_138), iVar7 == 0 && (local_122[0] != '\0'))) {
    if ((((-1 < (int)(local_130 << 0x1e)) &&
         ((((local_122[0] != '.' && (iVar7 = FUN_08056b1c((int)&local_130 + 1,0x2e), iVar7 != 0)) &&
           (*(char *)(iVar7 + 1) == 'W')) &&
          ((*(char *)(iVar7 + 2) == 'A' && (*(char *)(iVar7 + 3) == 'V')))))) &&
        ((local_130 & 0xffffff00) == uVar4)) &&
       ((iVar7 = FUN_08055818(auStack_12c), 0 < iVar7 &&
        (iVar8 = FUN_0801ee50(local_122,auStack_174,auStack_170), uVar5 = DAT_0801fac4, iVar8 == 0))
       )) {
      iVar8 = *(int *)(iVar3 + 8);
      piVar9[iVar8] = iVar7;
      *(int *)(iVar3 + 8) = iVar8 + 1;
      FUN_0804cb68(uVar5,uVar2,local_122);
    }
    iVar7 = FUN_080523c0(auStack_16c,auStack_138);
    if ((iVar7 != 0) || (local_122[0] == '\0')) break;
    if ((((-1 < (int)(local_130 << 0x1e)) &&
         (((local_122[0] != '.' && (iVar7 = FUN_08056b1c((int)&local_130 + 1,0x2e), iVar7 != 0)) &&
          (*(char *)(iVar7 + 1) == 'W')))) &&
        (((*(char *)(iVar7 + 2) == 'A' && (*(char *)(iVar7 + 3) == 'V')) &&
         ((local_130 & 0xffffff00) == uVar4)))) &&
       ((iVar7 = FUN_08055818(auStack_12c), 0 < iVar7 &&
        (iVar8 = FUN_0801ee50(local_122,auStack_174,auStack_170), uVar5 = DAT_0801fac4, iVar8 == 0))
       )) {
      iVar8 = *(int *)(iVar3 + 8);
      piVar9[iVar8] = iVar7;
      *(int *)(iVar3 + 8) = iVar8 + 1;
      FUN_0804cb68(uVar5,uVar2,local_122);
    }
    iVar6 = iVar6 + -2;
    if (iVar6 == 0) break;
  }
  FUN_0805234c(auStack_16c);
  piVar9 = DAT_0801fabc;
  iVar6 = *(int *)(iVar3 + 8);
  if ((iVar6 != 0) && (piVar11 = DAT_0801fabc + iVar6, piVar11 != DAT_0801fabc)) {
    iVar6 = (int)piVar11 - (int)DAT_0801fabc;
    FUN_0801db34(DAT_0801fabc,piVar11,(0x1f - LZCOUNT(iVar6 >> 2)) * 2);
    piVar12 = piVar9;
    if (iVar6 < 0x41) {
      while (piVar12 = piVar12 + 1, piVar11 != piVar12) {
        iVar6 = *piVar12;
        if (iVar6 < *piVar9) {
          FUN_08056330(piVar9 + 1,piVar9,(int)piVar12 - (int)piVar9);
          *piVar9 = iVar6;
        }
        else {
          iVar7 = piVar12[-1];
          piVar10 = piVar12 + -1;
          piVar13 = piVar12;
          while (piVar1 = piVar10, iVar6 < iVar7) {
            piVar1[1] = iVar7;
            piVar10 = piVar1 + -1;
            piVar13 = piVar1;
            iVar7 = piVar1[-1];
          }
          *piVar13 = iVar6;
        }
      }
    }
    else {
      piVar12 = piVar9 + 1;
      do {
        piVar13 = piVar12 + 1;
        iVar6 = *piVar12;
        if (iVar6 < *piVar9) {
          FUN_08056330(piVar9 + 1,piVar9,(int)piVar12 - (int)piVar9);
          *piVar9 = iVar6;
        }
        else {
          iVar7 = piVar12[-1];
          piVar10 = piVar12 + -1;
          while (piVar1 = piVar10, iVar6 < iVar7) {
            piVar1[1] = iVar7;
            piVar10 = piVar1 + -1;
            piVar12 = piVar1;
            iVar7 = piVar1[-1];
          }
          *piVar12 = iVar6;
        }
        piVar12 = piVar13;
      } while (piVar9 + 0x10 != piVar13);
      if (piVar11 != piVar9 + 0x10) {
        piVar9 = DAT_0801fac8 + 1;
        piVar12 = DAT_0801fac8;
        do {
          piVar10 = piVar9 + 1;
          iVar7 = *piVar9;
          iVar6 = *piVar12;
          piVar13 = piVar12;
          while (iVar7 < iVar6) {
            piVar13[1] = iVar6;
            iVar6 = piVar13[-1];
            piVar9 = piVar13;
            piVar13 = piVar13 + -1;
          }
          *piVar9 = iVar7;
          piVar9 = piVar10;
          piVar12 = piVar12 + 1;
        } while (piVar11 != piVar10);
      }
    }
    iVar6 = *(int *)(iVar3 + 8);
  }
  FUN_0804cb68(DAT_0801fac0,iVar6);
  return 0;
}


```

### callee `FUN_0802fbf0` @ `0802fbf0`
```c

undefined4 FUN_0802fbf0(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  undefined4 local_28;
  undefined4 uStack_24;
  int local_20;
  undefined4 local_1c;
  undefined4 local_18;
  
  iVar1 = DAT_0802fcb4;
  if (param_1 == 0) {
    *(uint *)(DAT_0802fcb4 + 0xe0) = *(uint *)(DAT_0802fcb4 + 0xe0) | 4;
    uVar3 = *(uint *)(iVar1 + 0xe0);
    *(uint *)(iVar1 + 0xe0) = *(uint *)(iVar1 + 0xe0) | 8;
    local_18 = 0xc;
    local_28 = 0x1f00;
    uStack_24 = 2;
    local_1c = 1;
    local_20 = param_1;
    FUN_08041424(DAT_0802fcb8,&local_28,0x1f00,1,uVar3 & 4,*(uint *)(iVar1 + 0xe0) & 8);
    local_18 = 0xc;
    local_28 = 4;
    uStack_24 = 2;
    local_20 = 0;
    local_1c = 1;
    FUN_08041424(DAT_0802fcbc,&local_28);
    *(uint *)(iVar1 + 0x7c) = *(uint *)(iVar1 + 0x7c) | 0x10000;
    *(uint *)(iVar1 + 0x7c) = *(uint *)(iVar1 + 0x7c) & 0xfffeffff;
    FUN_0803ec24(0x31,0xe,0);
    FUN_0803eca4(0x31);
    iVar1 = FUN_0802fbc0(DAT_0802fcc0);
    if ((iVar1 == 0) && (iVar1 = FUN_080448ac(DAT_0802fcc0,0x4000), iVar1 == 0)) {
      FUN_08044b30(DAT_0802fcc0,2);
      uVar2 = 0;
    }
    else {
      uVar2 = 0xfffffffc;
    }
    return uVar2;
  }
  return 0xfffffffe;
}


```

### callee `FUN_0803fb34` @ `0803fb34`
```c

undefined4 FUN_0803fb34(int *param_1)

{
  uint uVar1;
  int iVar2;
  
  if (param_1 == (int *)0x0) {
    return 1;
  }
  if (*(char *)((int)param_1 + 0x1d) == '\0') {
    *(undefined *)(param_1 + 7) = 0;
    FUN_0803fb30();
  }
  *(undefined *)((int)param_1 + 0x1d) = 2;
  if (*(char *)(param_1 + 1) == '\0') {
    iVar2 = *param_1;
    *(undefined4 *)(iVar2 + 0x14) = DAT_0803fbac;
    *(uint *)(iVar2 + 8) = *(uint *)(iVar2 + 8) & 0xffffffe7;
  }
  else {
    iVar2 = FUN_0803fddc(param_1,param_1[2],param_1[3]);
    if (iVar2 != 0) {
      return 1;
    }
    iVar2 = *param_1;
  }
  if (*(char *)((int)param_1 + 5) == '\0') {
    *(undefined4 *)(iVar2 + 0x10) = 0xffffffff;
  }
  else {
    *(int *)(iVar2 + 0x10) = param_1[4];
  }
  uVar1 = param_1[6];
  *(uint *)(iVar2 + 8) = *(uint *)(iVar2 + 8) & 0xffffff9f | param_1[5];
  *(uint *)(iVar2 + 8) = *(uint *)(iVar2 + 8) & 0xffffff7f | uVar1;
  *(undefined *)((int)param_1 + 0x1d) = 1;
  return 0;
}


```

---
## `FUN_0801fb94`  @ `0801fb94`
- **Anchors:** /Multigrain/Wavs
- **Strings seen:** /Multigrain/Wavs
- **Signature:** `undefined FUN_0801fb94(undefined param_1, undefined param_2, undefined param_3, undefined param_4, undefined4 param_5)`
- **Params:** 5  **Calls:** 8 funcs

```c

uint FUN_0801fb94(int param_1,char *param_2,undefined4 param_3,int param_4,uint *param_5)

{
  int *piVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  uint uVar4;
  int local_2c;
  uint local_28;
  uint local_24 [2];
  
  uVar3 = DAT_0801fcd0;
  uVar2 = DAT_0801fccc;
  piVar1 = DAT_0801fcc8;
  if (*DAT_0801fcc8 == 3) {
    return 1;
  }
  if (*param_2 == '\0') {
    return 4;
  }
  *DAT_0801fcc8 = 1;
  FUN_08051058(uVar3,uVar2);
  if (param_1 == 1) {
    local_28 = FUN_08051eb0(DAT_0801fce4);
  }
  else if (param_1 == 2) {
    local_28 = FUN_08051eb0(DAT_0801fcd4);
  }
  else {
    if ((param_1 != 0) || (*DAT_0801fcd8 < 0)) {
      uVar4 = 5;
      goto LAB_0801fbc6;
    }
    local_28 = FUN_08051eb0(DAT_0801fcdc);
  }
  uVar4 = local_28;
  if (local_28 == 0) {
    uVar4 = FUN_0801ee50(param_2,&local_2c,&local_28);
    if (uVar4 == 0) {
      if ((local_2c != 0) && (local_28 != 0)) {
        uVar4 = FUN_080510f0(DAT_0801fce0,param_2,1);
        if (uVar4 == 0) {
          *param_5 = 0;
          local_24[0] = uVar4;
          FUN_08051f1c(DAT_0801fce0,local_2c);
          uVar4 = local_28;
          if ((uint)(param_4 << 2) <= local_28) {
            uVar4 = param_4 << 2;
          }
          uVar4 = FUN_080513f8(DAT_0801fce0,param_3,uVar4,local_24);
          uVar2 = DAT_0801fce0;
          *param_5 = local_24[0] >> 2;
          if (uVar4 == 0) {
            FUN_08051d88(uVar2);
            *piVar1 = 0;
            return 0;
          }
          FUN_08051d88(uVar2);
          if (uVar4 != 1) {
            FUN_0801d860(uVar4);
            return uVar4;
          }
          goto LAB_0801fbf4;
        }
        FUN_08051d88(DAT_0801fce0);
        if (uVar4 == 1) goto LAB_0801fbf4;
        if (uVar4 != 0x12) {
          *piVar1 = 0;
          return uVar4;
        }
        goto LAB_0801fc6a;
      }
      FUN_08051d88(DAT_0801fce0);
      goto LAB_0801fbc6;
    }
    FUN_08051d88(DAT_0801fce0);
  }
  if (uVar4 == 1) {
LAB_0801fbf4:
    *piVar1 = 3;
    return 1;
  }
  if (uVar4 == 0x12) {
LAB_0801fc6a:
    *piVar1 = 2;
    return 0x12;
  }
LAB_0801fbc6:
  *piVar1 = 0;
  return uVar4;
}


```

---
## `FUN_0801fce8`  @ `0801fce8`
- **Anchors:** Rec%05d.wav
- **Strings seen:** Rec%05d.wav
- **Signature:** `undefined FUN_0801fce8()`
- **Params:** 0  **Calls:** 9 funcs

```c

int FUN_0801fce8(undefined4 param_1,int param_2)

{
  int *piVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  int local_19c;
  undefined auStack_198 [4];
  undefined2 local_194;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  undefined4 local_70;
  int iStack_6c;
  int local_68;
  int local_64;
  int local_60;
  undefined4 local_5c;
  undefined4 uStack_58;
  undefined *local_54;
  undefined4 uStack_50;
  undefined4 local_4c;
  undefined4 uStack_48;
  uint local_44;
  
  uVar3 = DAT_0801feb4;
  uVar2 = DAT_0801feb0;
  piVar1 = DAT_0801feac;
  if (*DAT_0801feac == 3) {
    return 1;
  }
  *DAT_0801feac = 1;
  FUN_08051058(uVar2,uVar3,1);
  local_19c = FUN_08051eb0(DAT_0801feb8);
  puVar5 = DAT_0801fef8;
  iVar7 = DAT_0801fef4;
  if (local_19c == 0) {
    iVar6 = *(int *)(DAT_0801fef4 + 8);
    if (iVar6 == 0x400) goto LAB_0801fdb0;
    if (iVar6 < 1) {
      *DAT_0801fef8 = 1;
      iVar8 = puVar5[iVar6];
      if (iVar8 < 0) {
        iVar8 = -iVar8;
      }
    }
    else {
      iVar8 = DAT_0801fef8[iVar6 + -1] + 1;
      if (DAT_0801febc <= DAT_0801fef8[iVar6 + -1] + 1) {
        iVar8 = DAT_0801febc;
      }
      if (iVar8 < 1) {
        iVar8 = 1;
      }
      DAT_0801fef8[iVar6] = iVar8;
    }
    FUN_080569f8(DAT_0801fec4,DAT_0801fec0,iVar8);
    FUN_0804cb68(DAT_0801fec8,DAT_0801fec4);
    local_19c = FUN_080510f0(DAT_0801fecc,DAT_0801fec4,6);
    if (local_19c == 0) {
      local_44 = DAT_0801fed0 & param_2 << 2;
      local_7c = local_44 + 0x38;
      local_80 = DAT_0801fed4;
      local_78 = DAT_0801fed4 + -0xf007fb;
      local_68 = DAT_0801fed8 + -0xb01fcf6;
      local_74 = DAT_0801fed4 + 0x5080bf8;
      local_64 = DAT_0801fed8 + -0x170203f1;
      local_70 = 0xc;
      iStack_6c = DAT_0801fed8;
      local_60 = DAT_0801fed8 + -0x53f9fbf5;
      local_5c = 0x10;
      uStack_58 = DAT_0801fedc;
      local_4c = DAT_0801fee8;
      uStack_48 = DAT_0801fee4;
      local_54 = &DAT_0000bb80;
      uStack_50 = DAT_0801fee0;
      iVar6 = FUN_08051884(DAT_0801fecc,&local_80,0x40,&local_19c);
      if (iVar6 != 0) {
        FUN_08051d88(DAT_0801fecc);
        if (iVar6 != 1) {
          if (iVar6 != 0x12) {
            *piVar1 = 0;
            return iVar6;
          }
          goto LAB_0801fdb0;
        }
        goto LAB_0801fd88;
      }
      iVar6 = FUN_08051884(DAT_0801fecc,param_1,param_2 << 2 & 0xffffffe0,&local_19c);
      if (iVar6 == 0) {
        *(int *)(iVar7 + 8) = *(int *)(iVar7 + 8) + 1;
      }
      puVar4 = DAT_0801feec;
      FUN_08051d88(DAT_0801fecc);
      FUN_08056428(auStack_198,0,0x118);
      local_194 = (undefined2)*puVar4;
      iVar6 = FUN_08052a38(DAT_0801fec4,auStack_198);
      iVar7 = *(int *)(iVar7 + 8) + -1;
      FUN_0804cb68(DAT_0801fef0,iVar7,puVar5[iVar7]);
      local_19c = iVar6;
    }
    else {
      FUN_08051d88(DAT_0801fecc);
    }
  }
  if (local_19c == 1) {
LAB_0801fd88:
    *piVar1 = 3;
    return 1;
  }
  if (local_19c != 0x12) {
    *piVar1 = 0;
    return local_19c;
  }
LAB_0801fdb0:
  *piVar1 = 2;
  return 0x12;
}


```

### callee `FUN_08052a38` @ `08052a38`
```c

int FUN_08052a38(undefined4 param_1,int param_2)

{
  undefined2 uVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 local_44;
  int local_40;
  int local_3c [8];
  int local_1c;
  byte local_d;
  
  local_44 = param_1;
  iVar3 = FUN_0804e3ac(&local_44,&local_40,2);
  local_3c[0] = local_40;
  if ((iVar3 == 0) && (iVar3 = FUN_0804fc10(local_3c,local_44), iVar3 == 0)) {
    if ((local_d & 0xa0) == 0) {
      uVar1 = *(undefined2 *)(param_2 + 4);
      uVar2 = *(undefined2 *)(param_2 + 6);
      *(char *)(local_1c + 0x16) = (char)uVar2;
      *(char *)(local_1c + 0x17) = (char)((ushort)uVar2 >> 8);
      *(char *)(local_1c + 0x18) = (char)uVar1;
      *(char *)(local_1c + 0x19) = (char)((ushort)uVar1 >> 8);
      *(undefined *)(local_40 + 3) = 1;
      iVar3 = FUN_0804ee7c();
    }
    else {
      iVar3 = 6;
    }
  }
  return iVar3;
}


```

---
## `FUN_08024414`  @ `08024414`
- **Anchors:** SD: Loading %s
- **Strings seen:** SD: Loading %s (%d bytes)...
- **Signature:** `undefined FUN_08024414()`
- **Params:** 0  **Calls:** 11 funcs

```c

int FUN_08024414(undefined4 param_1,undefined4 param_2)

{
  int *piVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  uint uVar5;
  int iVar6;
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 *local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  iVar6 = DAT_08024594;
  piVar1 = DAT_0802456c;
  if (*DAT_0802456c == 3) {
    return 1;
  }
  FUN_0804cb68(DAT_08024570,param_1,&DAT_000050dc);
  uVar2 = DAT_08024574;
  *piVar1 = 1;
  FUN_08051058(iVar6 + 4,uVar2,1);
  iVar3 = FUN_08051eb0(DAT_08024578);
  if (iVar3 != 0) {
    if (iVar3 != 1) {
      if (iVar3 == 0x12) {
        iVar6 = 2;
      }
      else {
        iVar6 = 0;
      }
      *piVar1 = iVar6;
      return iVar3;
    }
    *piVar1 = 3;
    return 1;
  }
  iVar3 = FUN_080510f0(iVar6 + 0x46c,param_1,1);
  if (iVar3 == 0) {
    local_40 = iVar3;
    iVar3 = FUN_080513f8(iVar6 + 0x46c,&local_3c,4,&local_40);
    if (iVar3 != 0) {
      FUN_08051d88(iVar6 + 0x46c);
      if (iVar3 == 1) goto LAB_080244ca;
      if (iVar3 != 0x12) goto LAB_080244c6;
      goto LAB_08024536;
    }
    FUN_08056428(DAT_0802457c,0,0x8000);
    uVar2 = DAT_0802457c;
    uVar5 = *(int *)(iVar6 + 0x478) - 4;
    if (0x7fff < uVar5) {
      uVar5 = 0x8000;
    }
    iVar3 = FUN_080513f8(iVar6 + 0x46c,DAT_0802457c,uVar5,&local_40);
    if (iVar3 == 0) {
      puVar4 = (undefined4 *)*DAT_08024580;
      if (*(code **)*puVar4 == DAT_08024584) {
        iVar6 = FUN_0803fbb0(puVar4 + 1,uVar2,0x2000);
      }
      else {
        iVar6 = (**(code **)*puVar4)(puVar4,uVar2,0x2000);
      }
      if (iVar6 != local_3c) {
        *piVar1 = 0;
        return 2;
      }
      local_34 = &local_30;
      local_2c = uVar2;
      local_24 = uVar2;
      local_30 = DAT_08024588;
      local_38 = 0;
      local_28 = DAT_0802458c;
      FUN_08023aec(param_2,&local_38);
      FUN_0804cb58(DAT_08024590);
      iVar3 = 0;
LAB_080244c6:
      *piVar1 = 0;
      return iVar3;
    }
  }
  else {
    FUN_08009ea4(param_2);
  }
  FUN_08051d88(iVar6 + 0x46c);
  if (iVar3 == 1) {
LAB_080244ca:
    *piVar1 = 3;
    return 1;
  }
  if (iVar3 != 0x12) {
    *piVar1 = 0;
    return iVar3;
  }
LAB_08024536:
  *piVar1 = 2;
  return 0x12;
}


```

### callee `FUN_08023aec` @ `08023aec`
```c

void FUN_08023aec(undefined *param_1,uint *param_2)

{
  code *pcVar1;
  undefined4 *puVar2;
  uint uVar3;
  char *pcVar4;
  int *piVar5;
  byte bVar6;
  byte bVar7;
  byte *pbVar8;
  float *pfVar9;
  byte *pbVar10;
  int iVar11;
  code *pcVar12;
  float *pfVar13;
  int *piVar14;
  undefined *puVar15;
  char cVar16;
  undefined *puVar17;
  char *pcVar18;
  float fVar19;
  byte local_22;
  byte local_21;
  undefined4 local_20;
  undefined4 local_1c;
  
  pcVar1 = DAT_08023dec;
  puVar2 = (undefined4 *)param_2[1];
  local_22 = 0x11;
  if (*(code **)*puVar2 == DAT_08023dec) {
    pbVar8 = (byte *)puVar2[2];
    pbVar10 = (byte *)puVar2[3];
    if (pbVar8 == pbVar10) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar2[2];
      pbVar10 = (byte *)puVar2[3];
    }
    local_22 = *pbVar10;
    puVar2[3] = pbVar10 + 1;
    if (pbVar8 < pbVar10 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_22,1);
  }
  FUN_0804cb68(DAT_08023df0,local_22);
  *param_2 = (uint)local_22;
  puVar17 = param_1;
  do {
    puVar15 = puVar17 + 0x9f0;
    FUN_08022d38(puVar17,param_2);
    puVar17 = puVar15;
  } while (puVar15 != &DAT_00004f80 + (int)param_1);
  puVar2 = (undefined4 *)param_2[1];
  local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00004f94)[(int)param_1]);
  if (*(code **)*puVar2 == pcVar1) {
    pcVar18 = (char *)puVar2[2];
    pcVar4 = (char *)puVar2[3];
    if (pcVar18 == pcVar4) {
      software_bkpt(0);
      pcVar18 = (char *)puVar2[2];
      pcVar4 = (char *)puVar2[3];
    }
    cVar16 = *pcVar4;
    local_20 = (float)CONCAT31(local_20._1_3_,cVar16);
    puVar2[3] = pcVar4 + 1;
    if (pcVar18 < pcVar4 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,1);
    cVar16 = (byte)local_20;
  }
  if (((&DAT_00004f94)[(int)param_1] != cVar16) &&
     ((&DAT_00004f94)[(int)param_1] = cVar16, *(int *)(&DAT_00004f8c + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar16);
    (**(code **)(&DAT_00004f90 + (int)param_1))(&UNK_00004f84 + (int)param_1,&local_1c);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00004fc4)[(int)param_1]);
  if (*(code **)*puVar2 == pcVar1) {
    pcVar18 = (char *)puVar2[2];
    pcVar4 = (char *)puVar2[3];
    if (pcVar18 == pcVar4) {
      software_bkpt(0);
      pcVar18 = (char *)puVar2[2];
      pcVar4 = (char *)puVar2[3];
    }
    cVar16 = *pcVar4;
    local_20 = (float)CONCAT31(local_20._1_3_,cVar16);
    puVar2[3] = pcVar4 + 1;
    if (pcVar18 < pcVar4 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,1);
    cVar16 = (byte)local_20;
  }
  if (((&DAT_00004fc4)[(int)param_1] != cVar16) &&
     ((&DAT_00004fc4)[(int)param_1] = cVar16, *(int *)(&DAT_00004fbc + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar16);
    (**(code **)(&DAT_00004fc0 + (int)param_1))(&UNK_00004fb4 + (int)param_1,&local_1c);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00004fac)[(int)param_1]);
  if (*(code **)*puVar2 == pcVar1) {
    pcVar18 = (char *)puVar2[2];
    pcVar4 = (char *)puVar2[3];
    if (pcVar18 == pcVar4) {
      software_bkpt(0);
      pcVar18 = (char *)puVar2[2];
      pcVar4 = (char *)puVar2[3];
    }
    cVar16 = *pcVar4;
    local_20 = (float)CONCAT31(local_20._1_3_,cVar16);
    puVar2[3] = pcVar4 + 1;
    if (pcVar18 < pcVar4 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,1);
    cVar16 = (byte)local_20;
  }
  if (((&DAT_00004fac)[(int)param_1] != cVar16) &&
     ((&DAT_00004fac)[(int)param_1] = cVar16, *(int *)(&DAT_00004fa4 + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar16);
    (**(code **)(&DAT_00004fa8 + (int)param_1))(&UNK_00004f9c + (int)param_1,&local_1c);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  local_20 = (float)CONCAT22(local_20._2_2_,*(undefined2 *)(&DAT_00004fd8 + (int)param_1));
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar6 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  uVar3 = (uint)local_1c;
  local_1c = (float)((uint)local_1c & 0xffffff00);
  puVar2 = (undefined4 *)param_2[1];
  if (bVar6 < 9) {
    local_20 = (float)CONCAT31(local_20._1_3_,bVar6);
  }
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar6 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  bVar7 = (byte)local_20;
  uVar3 = (uint)local_20 & 0xff;
  if (bVar6 < 9) {
    local_20._0_2_ = CONCAT11(bVar6,(byte)local_20);
  }
  if (((uVar3 < 9) && ((byte)(&DAT_00004fd8)[(int)param_1] != uVar3)) &&
     ((&DAT_00004fd8)[(int)param_1] = bVar7, *(int *)(&DAT_00004fd0 + (int)param_1) != 0)) {
    local_21 = bVar7;
    local_1c = 0.0;
    (**(code **)(&DAT_00004fd4 + (int)param_1))(&UNK_00004fc8 + (int)param_1,&local_1c,&local_21);
  }
  if (((local_20._1_1_ < 9) && ((&DAT_00004fd9)[(int)param_1] != local_20._1_1_)) &&
     ((&DAT_00004fd9)[(int)param_1] = local_20._1_1_, *(int *)(&DAT_00004fd0 + (int)param_1) != 0))
  {
    local_21 = local_20._1_1_;
    local_1c = 1.401298e-45;
    (**(code **)(&DAT_00004fd4 + (int)param_1))(&UNK_00004fc8 + (int)param_1,&local_1c,&local_21);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  bVar6 = (&DAT_00004ff5)[(int)param_1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar7 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar7 = (byte)local_1c;
  }
  if (((bVar7 < 2) || (bVar7 = bVar6, bVar6 < 2)) &&
     (((&DAT_00004ff5)[(int)param_1] != bVar7 &&
      ((&DAT_00004ff5)[(int)param_1] = bVar7, *(int *)(&DAT_00004fec + (int)param_1) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    (**(code **)(&DAT_00004ff0 + (int)param_1))(&UNK_00004fe4 + (int)param_1,&local_1c);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  bVar6 = (&DAT_0000500d)[(int)param_1];
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar7 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar7 = (byte)local_1c;
  }
  if ((((bVar7 < 2) || (bVar7 = bVar6, bVar6 < 2)) && ((&DAT_0000500d)[(int)param_1] != bVar7)) &&
     ((&DAT_0000500d)[(int)param_1] = bVar7, *(int *)(&DAT_00005004 + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    (**(code **)(&DAT_00005008 + (int)param_1))(&UNK_00004ffc + (int)param_1,&local_1c);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00005024)[(int)param_1]);
  if (*(code **)*puVar2 == pcVar1) {
    pcVar18 = (char *)puVar2[2];
    pcVar4 = (char *)puVar2[3];
    if (pcVar18 == pcVar4) {
      software_bkpt(0);
      pcVar18 = (char *)puVar2[2];
      pcVar4 = (char *)puVar2[3];
    }
    cVar16 = *pcVar4;
    local_20 = (float)CONCAT31(local_20._1_3_,cVar16);
    puVar2[3] = pcVar4 + 1;
    if (pcVar18 < pcVar4 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,1);
    cVar16 = (byte)local_20;
  }
  if (((&DAT_00005024)[(int)param_1] != cVar16) &&
     ((&DAT_00005024)[(int)param_1] = cVar16, *(int *)(&DAT_0000501c + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar16);
    (**(code **)(&DAT_00005020 + (int)param_1))(&UNK_00005014 + (int)param_1,&local_1c);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  bVar6 = (&DAT_0000503d)[(int)param_1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar7 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar7 = (byte)local_1c;
  }
  if (((bVar7 < 2) || (bVar7 = bVar6, bVar6 < 2)) &&
     (((&DAT_0000503d)[(int)param_1] != bVar7 &&
      ((&DAT_0000503d)[(int)param_1] = bVar7, *(int *)(&DAT_00005034 + (int)param_1) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    (**(code **)(&DAT_00005038 + (int)param_1))(&UNK_0000502c + (int)param_1,&local_1c);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  bVar6 = (&DAT_00005055)[(int)param_1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar7 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar7 = (byte)local_1c;
  }
  if ((((bVar7 < 2) || (bVar7 = bVar6, bVar6 < 2)) && ((&DAT_00005055)[(int)param_1] != bVar7)) &&
     ((&DAT_00005055)[(int)param_1] = bVar7, *(int *)(&DAT_0000504c + (int)param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    (**(code **)(&DAT_00005050 + (int)param_1))(&UNK_00005044 + (int)param_1,&local_1c);
  }
  uVar3 = (uint)local_1c;
  puVar2 = (undefined4 *)param_2[1];
  bVar6 = (&DAT_0000506d)[(int)param_1];
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar2 == pcVar1) {
    pbVar10 = (byte *)puVar2[2];
    pbVar8 = (byte *)puVar2[3];
    if (pbVar10 == pbVar8) {
      software_bkpt(0);
      pbVar10 = (byte *)puVar2[2];
      pbVar8 = (byte *)puVar2[3];
    }
    bVar7 = *pbVar8;
    local_1c._1_3_ = SUB43(uVar3,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    puVar2[3] = pbVar8 + 1;
    if (pbVar10 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_1c,1);
    bVar7 = (byte)local_1c;
  }
  if (((bVar7 < 2) || (bVar7 = bVar6, bVar6 < 2)) &&
     (((&DAT_0000506d)[(int)param_1] != bVar7 &&
      ((&DAT_0000506d)[(int)param_1] = bVar7, *(int *)(&DAT_00005064 + (int)param_1) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar7);
    (**(code **)(&DAT_00005068 + (int)param_1))(&UNK_0000505c + (int)param_1,&local_1c);
  }
  local_20 = *(float *)(&DAT_00005080 + (int)param_1);
  puVar2 = (undefined4 *)param_2[1];
  puVar17 = &UNK_00005070 + (int)param_1;
  if (*(code **)*puVar2 == pcVar1) {
    puVar15 = (undefined *)puVar2[3];
    if (puVar15 == (undefined *)puVar2[2]) {
      software_bkpt(0);
      puVar15 = (undefined *)puVar2[3];
    }
    local_20._1_3_ = (undefined3)((uint)local_20 >> 8);
    local_20 = (float)CONCAT31(local_20._1_3_,*puVar15);
    iVar11 = puVar2[3];
    puVar2[3] = iVar11 + 1U;
    if (iVar11 + 1U <= (uint)puVar2[2]) goto LAB_08023f12;
    software_bkpt(0);
    puVar2 = (undefined4 *)param_2[1];
    pcVar12 = *(code **)*puVar2;
    if (pcVar12 != pcVar1) goto LAB_080242de;
LAB_08023f1e:
    puVar15 = (undefined *)puVar2[3];
    if (puVar15 == (undefined *)puVar2[2]) {
      software_bkpt(0);
      puVar15 = (undefined *)puVar2[3];
    }
    local_20._0_2_ = CONCAT11(*puVar15,(byte)local_20);
    iVar11 = puVar2[3];
    puVar2[3] = iVar11 + 1U;
    if (iVar11 + 1U <= (uint)puVar2[2]) goto LAB_08023f40;
    software_bkpt(0);
    puVar2 = (undefined4 *)param_2[1];
    pcVar12 = *(code **)*puVar2;
    if (pcVar12 != pcVar1) goto LAB_080242c6;
LAB_08023f4c:
    puVar15 = (undefined *)puVar2[3];
    if (puVar15 == (undefined *)puVar2[2]) {
      software_bkpt(0);
      puVar15 = (undefined *)puVar2[3];
    }
    local_20._0_3_ = CONCAT12(*puVar15,(undefined2)local_20);
    iVar11 = puVar2[3];
    puVar2[3] = iVar11 + 1U;
    if ((uint)puVar2[2] < iVar11 + 1U) {
      software_bkpt(0);
      puVar2 = (undefined4 *)param_2[1];
      pcVar12 = *(code **)*puVar2;
      goto joined_r0x080242aa;
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,1);
LAB_08023f12:
    puVar2 = (undefined4 *)param_2[1];
    pcVar12 = *(code **)*puVar2;
    if (pcVar12 == pcVar1) goto LAB_08023f1e;
LAB_080242de:
    (*pcVar12)(puVar2,(int)&local_20 + 1,1);
LAB_08023f40:
    puVar2 = (undefined4 *)param_2[1];
    pcVar12 = *(code **)*puVar2;
    if (pcVar12 == pcVar1) goto LAB_08023f4c;
LAB_080242c6:
    (*pcVar12)(puVar2,(int)&local_20 + 2,1);
  }
  puVar2 = (undefined4 *)param_2[1];
  pcVar12 = *(code **)*puVar2;
joined_r0x080242aa:
  if (pcVar12 == pcVar1) {
    puVar15 = (undefined *)puVar2[3];
    if ((undefined *)puVar2[2] == puVar15) {
      software_bkpt(0);
      puVar15 = (undefined *)puVar2[3];
    }
    local_20 = (float)CONCAT13(*puVar15,(undefined3)local_20);
    iVar11 = puVar2[3];
    puVar2[3] = iVar11 + 1U;
    if ((uint)puVar2[2] < iVar11 + 1U) {
      software_bkpt(0);
    }
  }
  else {
    (*pcVar12)(puVar2,(int)&local_20 + 3,1);
  }
  uVar3 = (uint)local_20 & 0xff;
  if ((((byte)(&DAT_00005085)[(int)param_1] <= uVar3) &&
      (uVar3 <= (byte)(&DAT_00005086)[(int)param_1])) &&
     (((byte)(&DAT_00005080)[(int)param_1] != uVar3 &&
      ((&DAT_00005080)[(int)param_1] = (byte)local_20, *(int *)(&DAT_00005078 + (int)param_1) != 0))
     )) {
    local_21 = (byte)local_20;
    local_1c = 0.0;
    (**(code **)(&DAT_0000507c + (int)param_1))(puVar17,&local_1c,&local_21);
  }
  if (((((byte)(&DAT_00005085)[(int)param_1] <= local_20._1_1_) &&
       (local_20._1_1_ <= (byte)(&DAT_00005086)[(int)param_1])) &&
      ((&DAT_00005081)[(int)param_1] != local_20._1_1_)) &&
     ((&DAT_00005081)[(int)param_1] = local_20._1_1_, *(int *)(&DAT_00005078 + (int)param_1) != 0))
  {
    local_21 = local_20._1_1_;
    local_1c = 1.401298e-45;
    (**(code **)(&DAT_0000507c + (int)param_1))(puVar17,&local_1c,&local_21);
  }
  if ((((byte)(&DAT_00005085)[(int)param_1] <= local_20._2_1_) &&
      (local_20._2_1_ <= (byte)(&DAT_00005086)[(int)param_1])) &&
     (((&DAT_00005082)[(int)param_1] != local_20._2_1_ &&
      ((&DAT_00005082)[(int)param_1] = local_20._2_1_, *(int *)(&DAT_00005078 + (int)param_1) != 0))
     )) {
    local_21 = local_20._2_1_;
    local_1c = 2.802597e-45;
    (**(code **)(&DAT_0000507c + (int)param_1))(puVar17,&local_1c,&local_21);
  }
  if ((((byte)(&DAT_00005085)[(int)param_1] <= local_20._3_1_) &&
      (local_20._3_1_ <= (byte)(&DAT_00005086)[(int)param_1])) &&
     (((&DAT_00005083)[(int)param_1] != local_20._3_1_ &&
      ((&DAT_00005083)[(int)param_1] = local_20._3_1_, *(int *)(&DAT_00005078 + (int)param_1) != 0))
     )) {
    local_21 = local_20._3_1_;
    local_1c = 4.203895e-45;
    (**(code **)(&DAT_0000507c + (int)param_1))(puVar17,&local_1c,&local_21);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = *(float *)(&DAT_000050a0 + (int)param_1);
  if (*(code **)*puVar2 == pcVar1) {
    pfVar9 = (float *)puVar2[2];
    pfVar13 = (float *)puVar2[3];
    if ((uint)((int)pfVar9 - (int)pfVar13) < 4) {
      software_bkpt(0);
      pfVar9 = (float *)puVar2[2];
      pfVar13 = (float *)puVar2[3];
    }
    local_20 = *pfVar13;
    puVar2[3] = pfVar13 + 1;
    if (pfVar9 < pfVar13 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,4);
  }
  if ((((local_20 < *(float *)(&DAT_000050a4 + (int)param_1) ==
         (NAN(local_20) || NAN(*(float *)(&DAT_000050a4 + (int)param_1)))) &&
       (fVar19 = *(float *)(&DAT_000050a8 + (int)param_1),
       local_20 == fVar19 || local_20 < fVar19 != (NAN(local_20) || NAN(fVar19)))) &&
      (local_20 != *(float *)(&DAT_000050a0 + (int)param_1))) &&
     (*(float *)(&DAT_000050a0 + (int)param_1) = local_20,
     *(int *)(&DAT_00005094 + (int)param_1) != 0)) {
    local_1c = local_20;
    (**(code **)(&DAT_00005098 + (int)param_1))(&UNK_0000508c + (int)param_1,&local_1c);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = *(float *)(&DAT_000050c0 + (int)param_1);
  if (*(code **)*puVar2 == pcVar1) {
    pfVar9 = (float *)puVar2[2];
    pfVar13 = (float *)puVar2[3];
    if ((uint)((int)pfVar9 - (int)pfVar13) < 4) {
      software_bkpt(0);
      pfVar9 = (float *)puVar2[2];
      pfVar13 = (float *)puVar2[3];
    }
    local_20 = *pfVar13;
    puVar2[3] = pfVar13 + 1;
    if (pfVar9 < pfVar13 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,4);
  }
  if ((*(float *)(&DAT_000050c0 + (int)param_1) != local_20) &&
     (*(float *)(&DAT_000050c0 + (int)param_1) = local_20,
     *(int *)(&DAT_000050b8 + (int)param_1) != 0)) {
    local_1c = local_20;
    (**(code **)(&DAT_000050bc + (int)param_1))(&UNK_000050b0 + (int)param_1,&local_1c);
  }
  puVar2 = (undefined4 *)param_2[1];
  local_20 = *(float *)(&DAT_000050d8 + (int)param_1);
  if (*(code **)*puVar2 == pcVar1) {
    piVar5 = (int *)puVar2[2];
    piVar14 = (int *)puVar2[3];
    if ((uint)((int)piVar5 - (int)piVar14) < 4) {
      software_bkpt(0);
      piVar5 = (int *)puVar2[2];
      piVar14 = (int *)puVar2[3];
    }
    local_20 = (float)*piVar14;
    puVar2[3] = piVar14 + 1;
    if (piVar5 < piVar14 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar2)(puVar2,&local_20,4);
  }
  if ((local_20 != (float)*(int *)(&DAT_000050d8 + (int)param_1)) &&
     (*(float *)(&DAT_000050d8 + (int)param_1) = local_20,
     *(int *)(&DAT_000050d0 + (int)param_1) != 0)) {
    local_1c = local_20;
    (**(code **)(&DAT_000050d4 + (int)param_1))(&UNK_000050c8 + (int)param_1,&local_1c);
  }
  return;
}


```

### callee `FUN_08009ea4` @ `08009ea4`
```c

void FUN_08009ea4(int param_1)

{
  undefined local_19;
  undefined4 local_18;
  undefined4 local_14;
  
  local_18 = 0x11;
  FUN_08009be0(param_1,&local_18);
  if (((&DAT_00004fd8)[param_1] != '\0') &&
     ((&DAT_00004fd8)[param_1] = 0, *(int *)(&DAT_00004fd0 + param_1) != 0)) {
    local_14 = 0;
    local_19 = 0;
    (**(code **)(&DAT_00004fd4 + param_1))(&UNK_00004fc8 + param_1,&local_14,&local_19);
  }
  if (((&DAT_00004fd9)[param_1] != '\x01') &&
     ((&DAT_00004fd9)[param_1] = 1, *(int *)(&DAT_00004fd0 + param_1) != 0)) {
    local_14 = 1;
    local_19 = 1;
    (**(code **)(&DAT_00004fd4 + param_1))(&UNK_00004fc8 + param_1,&local_14,&local_19);
  }
  return;
}


```

### callee `FUN_0803fbb0` @ `0803fbb0`
```c

undefined4 FUN_0803fbb0(undefined4 *param_1,undefined4 *param_2,uint param_3)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  uint uVar7;
  undefined4 uVar8;
  uint uVar9;
  undefined2 *puVar10;
  undefined4 *puVar11;
  uint uVar12;
  undefined4 *puVar13;
  int iVar14;
  int iVar15;
  int iVar16;
  undefined4 *puVar17;
  int iVar18;
  int iVar19;
  
  *(undefined *)((int)param_1 + 0x1d) = 2;
  puVar13 = (undefined4 *)*param_1;
  iVar14 = param_1[8];
  puVar13[2] = puVar13[2] | 1;
  if (iVar14 != 2) {
    if (iVar14 != 3) {
      if (iVar14 == 1) {
        uVar8 = FUN_0803f9e8();
        *(undefined *)((int)param_1 + 0x1d) = 1;
        return uVar8;
      }
      *(undefined *)((int)param_1 + 0x1d) = 1;
      return 0;
    }
    if (param_3 != 0) {
      puVar17 = param_2 + -1;
      puVar11 = puVar17 + param_3;
      uVar9 = (param_3 * 4 - 4 >> 2) + 1 & 7;
      if (uVar9 != 0) {
        if (uVar9 != 1) {
          if (uVar9 != 2) {
            if (uVar9 != 3) {
              if (uVar9 != 4) {
                if (uVar9 != 5) {
                  if (uVar9 != 6) {
                    *puVar13 = *param_2;
                    puVar17 = param_2;
                  }
                  puVar17 = puVar17 + 1;
                  *puVar13 = *puVar17;
                }
                puVar17 = puVar17 + 1;
                *puVar13 = *puVar17;
              }
              puVar17 = puVar17 + 1;
              *puVar13 = *puVar17;
            }
            puVar17 = puVar17 + 1;
            *puVar13 = *puVar17;
          }
          puVar17 = puVar17 + 1;
          *puVar13 = *puVar17;
        }
        puVar17 = puVar17 + 1;
        *puVar13 = *puVar17;
        if (puVar11 == puVar17) goto LAB_0803fd1c;
      }
      do {
        *puVar13 = puVar17[1];
        *puVar13 = puVar17[2];
        *puVar13 = puVar17[3];
        *puVar13 = puVar17[4];
        *puVar13 = puVar17[5];
        *puVar13 = puVar17[6];
        *puVar13 = puVar17[7];
        puVar17 = puVar17 + 8;
        *puVar13 = *puVar17;
      } while (puVar11 != puVar17);
    }
    goto LAB_0803fd1c;
  }
  uVar9 = param_3 >> 1;
  if (uVar9 != 0) {
    uVar7 = uVar9 & 7;
    uVar12 = 0;
    puVar10 = (undefined2 *)((int)param_2 + 2);
    if (uVar7 != 0) {
      if (uVar7 != 1) {
        if (uVar7 != 2) {
          if (uVar7 != 3) {
            if (uVar7 != 4) {
              if (uVar7 != 5) {
                if (uVar7 != 6) {
                  *puVar13 = CONCAT22(*(undefined2 *)param_2,*puVar10);
                }
                uVar7 = (uint)(uVar7 != 6);
                uVar12 = uVar7 + 1;
                *puVar13 = CONCAT22(*(undefined2 *)(param_2 + uVar7),puVar10[uVar7 * 2]);
              }
              puVar17 = param_2 + uVar12;
              iVar14 = uVar12 * 2;
              uVar12 = uVar12 + 1;
              *puVar13 = CONCAT22(*(undefined2 *)puVar17,puVar10[iVar14]);
            }
            puVar17 = param_2 + uVar12;
            iVar14 = uVar12 * 2;
            uVar12 = uVar12 + 1;
            *puVar13 = CONCAT22(*(undefined2 *)puVar17,puVar10[iVar14]);
          }
          puVar17 = param_2 + uVar12;
          iVar14 = uVar12 * 2;
          uVar12 = uVar12 + 1;
          *puVar13 = CONCAT22(*(undefined2 *)puVar17,puVar10[iVar14]);
        }
        puVar17 = param_2 + uVar12;
        iVar14 = uVar12 * 2;
        uVar12 = uVar12 + 1;
        *puVar13 = CONCAT22(*(undefined2 *)puVar17,puVar10[iVar14]);
      }
      puVar17 = param_2 + uVar12;
      iVar14 = uVar12 * 2;
      uVar12 = uVar12 + 1;
      *puVar13 = CONCAT22(*(undefined2 *)puVar17,puVar10[iVar14]);
      if (uVar12 == uVar9) goto LAB_0803fd10;
    }
    do {
      iVar16 = uVar12 + 3;
      iVar19 = uVar12 + 4;
      uVar1 = *(undefined2 *)(param_2 + uVar12 + 1);
      uVar2 = puVar10[(uVar12 + 1) * 2];
      iVar18 = uVar12 + 5;
      *puVar13 = CONCAT22(*(undefined2 *)(param_2 + uVar12),puVar10[uVar12 * 2]);
      iVar15 = uVar12 + 6;
      uVar3 = *(undefined2 *)(param_2 + uVar12 + 2);
      uVar4 = puVar10[(uVar12 + 2) * 2];
      iVar14 = uVar12 + 7;
      uVar5 = *(undefined2 *)(param_2 + iVar16);
      uVar12 = uVar12 + 8;
      *puVar13 = CONCAT22(uVar1,uVar2);
      uVar1 = puVar10[iVar16 * 2];
      uVar2 = *(undefined2 *)(param_2 + iVar19);
      *puVar13 = CONCAT22(uVar3,uVar4);
      uVar3 = puVar10[iVar19 * 2];
      *puVar13 = CONCAT22(uVar5,uVar1);
      uVar1 = *(undefined2 *)(param_2 + iVar18);
      uVar4 = puVar10[iVar18 * 2];
      uVar5 = *(undefined2 *)(param_2 + iVar15);
      uVar6 = puVar10[iVar15 * 2];
      *puVar13 = CONCAT22(uVar2,uVar3);
      uVar2 = *(undefined2 *)(param_2 + iVar14);
      uVar3 = puVar10[iVar14 * 2];
      *puVar13 = CONCAT22(uVar1,uVar4);
      *puVar13 = CONCAT22(uVar5,uVar6);
      *puVar13 = CONCAT22(uVar2,uVar3);
    } while (uVar12 != uVar9);
  }
LAB_0803fd10:
  if ((param_3 & 1) != 0) {
    *(undefined2 *)puVar13 = *(undefined2 *)(param_2 + uVar9);
  }
LAB_0803fd1c:
  uVar8 = *puVar13;
  *(undefined *)((int)param_1 + 0x1d) = 1;
  return uVar8;
}


```

---
## `FUN_08026754`  @ `08026754`
- **Anchors:** SD: Loading %s
- **Strings seen:** SD: Loading %s (%d bytes)...
- **Signature:** `undefined FUN_08026754()`
- **Params:** 0  **Calls:** 12 funcs

```c

int FUN_08026754(uint param_1,int param_2)

{
  undefined4 uVar1;
  int *piVar2;
  int iVar3;
  undefined4 *puVar4;
  uint uVar5;
  int iVar6;
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 *local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  piVar2 = DAT_08026954;
  FUN_080569f8(DAT_08026924,DAT_08026928,param_1 + 1);
  iVar6 = DAT_08026958;
  if (*piVar2 == 3) {
    return 1;
  }
  FUN_0804cb68(DAT_0802692c,DAT_08026924,&DAT_000050dc);
  uVar1 = DAT_08026930;
  *piVar2 = 1;
  FUN_08051058(iVar6 + 4,uVar1,1);
  iVar3 = FUN_08051eb0(DAT_08026934);
  if (iVar3 != 0) {
    if (iVar3 != 1) {
      if (iVar3 == 0x12) {
        iVar6 = 2;
      }
      else {
        iVar6 = 0;
      }
      *piVar2 = iVar6;
      return iVar3;
    }
    *piVar2 = 3;
    return 1;
  }
  iVar3 = FUN_080510f0(iVar6 + 0x46c,DAT_08026924,1);
  if (iVar3 == 0) {
    local_40 = iVar3;
    iVar3 = FUN_080513f8(iVar6 + 0x46c,&local_3c,4,&local_40);
    if (iVar3 != 0) {
      FUN_08051d88(iVar6 + 0x46c);
      if (iVar3 == 1) goto LAB_08026820;
      if (iVar3 != 0x12) {
        *piVar2 = 0;
        return iVar3;
      }
      goto LAB_08026910;
    }
    FUN_08056428(DAT_08026938,0,0x8000);
    uVar1 = DAT_08026938;
    uVar5 = *(int *)(iVar6 + 0x478) - 4;
    if (0x7fff < uVar5) {
      uVar5 = 0x8000;
    }
    iVar3 = FUN_080513f8(iVar6 + 0x46c,DAT_08026938,uVar5,&local_40);
    if (iVar3 == 0) {
      puVar4 = (undefined4 *)*DAT_0802693c;
      if (*(code **)*puVar4 == DAT_08026940) {
        iVar6 = FUN_0803fbb0(puVar4 + 1,uVar1,0x2000);
      }
      else {
        iVar6 = (**(code **)*puVar4)(puVar4,uVar1,0x2000);
      }
      if (iVar6 != local_3c) {
        *piVar2 = 0;
        return 2;
      }
      local_2c = uVar1;
      local_24 = uVar1;
      local_30 = DAT_08026944;
      local_28 = DAT_08026948;
      local_38 = 0;
      local_34 = &local_30;
      FUN_08023aec(param_2,&local_38);
      FUN_0804cb58(DAT_0802694c);
      *piVar2 = 0;
      if (**(code ***)(&DAT_00004f80 + param_2) != DAT_08026950) {
        (***(code ***)(&DAT_00004f80 + param_2))(&DAT_00004f80 + param_2,param_1 & 0xff);
        return 0;
      }
      if ((uint)(byte)(&DAT_00004f94)[param_2] == (param_1 & 0xff)) {
        return 0;
      }
      (&DAT_00004f94)[param_2] = (char)param_1;
      if (*(int *)(&DAT_00004f8c + param_2) == 0) {
        return 0;
      }
      local_30 = CONCAT31(local_30._1_3_,(char)param_1);
      (**(code **)(&DAT_00004f90 + param_2))(&UNK_00004f84 + param_2,&local_30);
      return 0;
    }
  }
  else {
    FUN_08009ea4(param_2);
  }
  FUN_08051d88(iVar6 + 0x46c);
  if (iVar3 == 1) {
LAB_08026820:
    *piVar2 = 3;
    return 1;
  }
  if (iVar3 != 0x12) {
    *piVar2 = 0;
    return iVar3;
  }
LAB_08026910:
  *piVar2 = 2;
  return 0x12;
}


```

---
## `FUN_080277ac`  @ `080277ac`
- **Anchors:** SD: Loading %s
- **Strings seen:** SD: Loading %s (%d bytes)...
- **Signature:** `undefined FUN_080277ac()`
- **Params:** 0  **Calls:** 11 funcs

```c

int FUN_080277ac(undefined4 param_1)

{
  int *piVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  int iVar5;
  uint uVar6;
  int local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 *local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  iVar5 = DAT_08027938;
  piVar1 = DAT_0802790c;
  if (*DAT_0802790c == 3) {
    return 1;
  }
  FUN_0804cb68(DAT_08027914,DAT_08027910,&DAT_00001650);
  uVar2 = DAT_08027918;
  *piVar1 = 1;
  FUN_08051058(iVar5 + 4,uVar2,1);
  iVar3 = FUN_08051eb0(DAT_0802791c);
  if (iVar3 != 0) {
    if (iVar3 == 1) goto LAB_08027854;
    if (iVar3 != 0x12) {
      *piVar1 = 0;
      return iVar3;
    }
    goto LAB_08027862;
  }
  iVar3 = FUN_080510f0(iVar5 + 0x46c,DAT_08027910,1);
  if (iVar3 == 0) {
    local_40 = iVar3;
    iVar3 = FUN_080513f8(iVar5 + 0x46c,&local_3c,4,&local_40);
    if (iVar3 == 0) {
      FUN_08056428(DAT_08027920,0,0x2000);
      uVar2 = DAT_08027920;
      uVar6 = *(int *)(iVar5 + 0x478) - 4;
      if (0x1fff < uVar6) {
        uVar6 = 0x2000;
      }
      iVar3 = FUN_080513f8(iVar5 + 0x46c,DAT_08027920,uVar6,&local_40);
      if (iVar3 != 0) {
        FUN_08051d88(iVar5 + 0x46c);
        goto joined_r0x080278d8;
      }
      puVar4 = (undefined4 *)*DAT_08027924;
      if (*(code **)*puVar4 == DAT_08027928) {
        iVar5 = FUN_0803fbb0(puVar4 + 1,uVar2,0x800);
      }
      else {
        iVar5 = (**(code **)*puVar4)(puVar4,uVar2,0x800);
      }
      if (local_3c != iVar5) {
        *piVar1 = 0;
        return 2;
      }
      local_34 = &local_30;
      local_2c = uVar2;
      local_24 = uVar2;
      local_30 = DAT_0802792c;
      local_38 = 0;
      local_28 = DAT_08027930;
      FUN_0802695c(param_1,&local_38);
      FUN_0804cb58(DAT_08027934);
    }
    else {
      FUN_08051d88(iVar5 + 0x46c);
      if (iVar3 == 1) goto LAB_08027854;
      if (iVar3 == 0x12) goto LAB_08027862;
    }
    *piVar1 = 0;
  }
  else {
    FUN_08009bcc(param_1);
    FUN_08051d88(iVar5 + 0x46c);
joined_r0x080278d8:
    if (iVar3 == 1) {
LAB_08027854:
      *piVar1 = 3;
      return 1;
    }
    if (iVar3 == 0x12) {
LAB_08027862:
      *piVar1 = 2;
      return 0x12;
    }
    *piVar1 = 0;
  }
  return iVar3;
}


```

### callee `FUN_0802695c` @ `0802695c`
```c

void FUN_0802695c(int param_1,uint *param_2)

{
  code *pcVar1;
  uint uVar2;
  undefined4 *puVar3;
  char *pcVar4;
  float *pfVar5;
  byte bVar6;
  byte *pbVar7;
  byte *pbVar8;
  float *pfVar9;
  char cVar10;
  byte bVar11;
  char *pcVar12;
  undefined4 in_cr3;
  undefined4 in_cr4;
  undefined4 in_cr5;
  undefined4 in_cr6;
  float fVar13;
  byte local_21;
  undefined4 local_20;
  undefined4 local_1c;
  
  pcVar1 = DAT_08026c28;
  puVar3 = (undefined4 *)param_2[1];
  local_21 = 0x11;
  if (*(code **)*puVar3 == DAT_08026c28) {
    pbVar7 = (byte *)puVar3[2];
    pbVar8 = (byte *)puVar3[3];
    if (pbVar7 == pbVar8) {
      software_bkpt(0);
      pbVar7 = (byte *)puVar3[2];
      pbVar8 = (byte *)puVar3[3];
    }
    local_21 = *pbVar8;
    puVar3[3] = pbVar8 + 1;
    if (pbVar7 < pbVar8 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_21,1);
  }
  FUN_0804cb68(DAT_08026c2c,local_21);
  puVar3 = (undefined4 *)param_2[1];
  *param_2 = (uint)local_21;
  local_20 = (float)CONCAT31(local_20._1_3_,*(undefined *)(param_1 + 0x14));
  if (*(code **)*puVar3 == pcVar1) {
    pcVar12 = (char *)puVar3[2];
    pcVar4 = (char *)puVar3[3];
    if (pcVar12 == pcVar4) {
      software_bkpt(0);
      pcVar12 = (char *)puVar3[2];
      pcVar4 = (char *)puVar3[3];
    }
    cVar10 = *pcVar4;
    local_20 = (float)CONCAT31(local_20._1_3_,cVar10);
    puVar3[3] = pcVar4 + 1;
    if (pcVar12 < pcVar4 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,1);
    cVar10 = (byte)local_20;
  }
  if ((*(char *)(param_1 + 0x14) != cVar10) &&
     (*(char *)(param_1 + 0x14) = cVar10, *(int *)(param_1 + 0xc) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
    (**(code **)(param_1 + 0x10))(param_1 + 4,&local_1c);
  }
  puVar3 = (undefined4 *)param_2[1];
  local_20 = *(float *)(param_1 + 0x2c);
  if (*(code **)*puVar3 == pcVar1) {
    pfVar5 = (float *)puVar3[2];
    pfVar9 = (float *)puVar3[3];
    if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
      software_bkpt(0);
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
    }
    local_20 = *pfVar9;
    puVar3[3] = pfVar9 + 1;
    if (pfVar5 < pfVar9 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,4);
  }
  if ((*(float *)(param_1 + 0x2c) != local_20) &&
     (*(float *)(param_1 + 0x2c) = local_20, *(int *)(param_1 + 0x24) != 0)) {
    local_1c = local_20;
    (**(code **)(param_1 + 0x28))(param_1 + 0x1c,&local_1c);
  }
  puVar3 = (undefined4 *)param_2[1];
  local_20 = *(float *)(param_1 + 0x48);
  if (*(code **)*puVar3 == pcVar1) {
    pfVar5 = (float *)puVar3[2];
    pfVar9 = (float *)puVar3[3];
    if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
      software_bkpt(0);
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
    }
    local_20 = *pfVar9;
    puVar3[3] = pfVar9 + 1;
    if (pfVar5 < pfVar9 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,4);
  }
  if ((((local_20 < *(float *)(param_1 + 0x4c) == (NAN(local_20) || NAN(*(float *)(param_1 + 0x4c)))
        ) && (fVar13 = *(float *)(param_1 + 0x50),
             local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
      (local_20 != *(float *)(param_1 + 0x48))) &&
     (*(float *)(param_1 + 0x48) = local_20, *(int *)(param_1 + 0x3c) != 0)) {
    local_1c = local_20;
    (**(code **)(param_1 + 0x40))(param_1 + 0x34,&local_1c);
  }
  fVar13 = local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x69);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(fVar13,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 3) || (bVar6 = bVar11, bVar11 < 3)) &&
     ((*(byte *)(param_1 + 0x69) != bVar6 &&
      (*(byte *)(param_1 + 0x69) = bVar6, *(int *)(param_1 + 0x60) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 100))(param_1 + 0x58,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x81);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
     ((*(byte *)(param_1 + 0x81) != bVar6 &&
      (*(byte *)(param_1 + 0x81) = bVar6, *(int *)(param_1 + 0x78) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x7c))(param_1 + 0x70,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x99);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if ((((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) && (*(byte *)(param_1 + 0x99) != bVar6)) &&
     (*(byte *)(param_1 + 0x99) = bVar6, *(int *)(param_1 + 0x90) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x94))(param_1 + 0x88,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0xb1);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 4) || (bVar6 = bVar11, bVar11 < 4)) &&
     ((*(byte *)(param_1 + 0xb1) != bVar6 &&
      (*(byte *)(param_1 + 0xb1) = bVar6, *(int *)(param_1 + 0xa8) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0xac))(param_1 + 0xa0,&local_1c);
  }
  puVar3 = (undefined4 *)param_2[1];
  local_20 = *(float *)(param_1 + 0xcc);
  if (*(code **)*puVar3 == pcVar1) {
    pfVar5 = (float *)puVar3[2];
    pfVar9 = (float *)puVar3[3];
    if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
      software_bkpt(0);
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
    }
    local_20 = *pfVar9;
    puVar3[3] = pfVar9 + 1;
    if (pfVar5 < pfVar9 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,4);
  }
  if (((local_20 < *(float *)(param_1 + 0xd0) == (NAN(local_20) || NAN(*(float *)(param_1 + 0xd0))))
      && (fVar13 = *(float *)(param_1 + 0xd4),
         local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
     ((local_20 != *(float *)(param_1 + 0xcc) &&
      (*(float *)(param_1 + 0xcc) = local_20, *(int *)(param_1 + 0xc0) != 0)))) {
    local_1c = local_20;
    (**(code **)(param_1 + 0xc4))(param_1 + 0xb8,&local_1c);
  }
  puVar3 = (undefined4 *)param_2[1];
  local_20 = *(float *)(param_1 + 0xf0);
  if (*(code **)*puVar3 == pcVar1) {
    pfVar5 = (float *)puVar3[2];
    pfVar9 = (float *)puVar3[3];
    if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
      software_bkpt(0);
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
    }
    local_20 = *pfVar9;
    puVar3[3] = pfVar9 + 1;
    if (pfVar5 < pfVar9 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,4);
  }
  if ((((local_20 < *(float *)(param_1 + 0xf4) == (NAN(local_20) || NAN(*(float *)(param_1 + 0xf4)))
        ) && (fVar13 = *(float *)(param_1 + 0xf8),
             local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
      (local_20 != *(float *)(param_1 + 0xf0))) &&
     (*(float *)(param_1 + 0xf0) = local_20, *(int *)(param_1 + 0xe4) != 0)) {
    local_1c = local_20;
    (**(code **)(param_1 + 0xe8))(param_1 + 0xdc,&local_1c);
  }
  puVar3 = (undefined4 *)param_2[1];
  local_20 = *(float *)(param_1 + 0x114);
  if (*(code **)*puVar3 == pcVar1) {
    pfVar5 = (float *)puVar3[2];
    pfVar9 = (float *)puVar3[3];
    if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
      software_bkpt(0);
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
    }
    local_20 = *pfVar9;
    puVar3[3] = pfVar9 + 1;
    if (pfVar5 < pfVar9 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_20,4);
  }
  if (((local_20 < *(float *)(param_1 + 0x118) ==
        (NAN(local_20) || NAN(*(float *)(param_1 + 0x118)))) &&
      (fVar13 = *(float *)(param_1 + 0x11c),
      local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
     ((local_20 != *(float *)(param_1 + 0x114) &&
      (*(float *)(param_1 + 0x114) = local_20, *(int *)(param_1 + 0x108) != 0)))) {
    local_1c = local_20;
    (**(code **)(param_1 + 0x10c))(param_1 + 0x100,&local_1c);
  }
  fVar13 = local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x135);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(fVar13,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
     ((*(byte *)(param_1 + 0x135) != bVar6 &&
      (*(byte *)(param_1 + 0x135) = bVar6, *(int *)(param_1 + 300) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x130))(param_1 + 0x124,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x14d);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if ((((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) && (*(byte *)(param_1 + 0x14d) != bVar6)) &&
     (*(byte *)(param_1 + 0x14d) = bVar6, *(int *)(param_1 + 0x144) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x148))(param_1 + 0x13c,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x165);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 4) || (bVar6 = bVar11, bVar11 < 4)) &&
     ((*(byte *)(param_1 + 0x165) != bVar6 &&
      (*(byte *)(param_1 + 0x165) = bVar6, *(int *)(param_1 + 0x15c) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x160))(param_1 + 0x154,&local_1c);
  }
  uVar2 = (uint)local_1c;
  puVar3 = (undefined4 *)param_2[1];
  bVar11 = *(byte *)(param_1 + 0x17d);
  local_1c = (float)((uint)local_1c & 0xffffff00);
  if (*(code **)*puVar3 == pcVar1) {
    pbVar8 = (byte *)puVar3[2];
    pbVar7 = (byte *)puVar3[3];
    if (pbVar8 == pbVar7) {
      software_bkpt(0);
      pbVar8 = (byte *)puVar3[2];
      pbVar7 = (byte *)puVar3[3];
    }
    bVar6 = *pbVar7;
    local_1c._1_3_ = SUB43(uVar2,1);
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    puVar3[3] = pbVar7 + 1;
    if (pbVar8 < pbVar7 + 1) {
      software_bkpt(0);
    }
  }
  else {
    (**(code **)*puVar3)(puVar3,&local_1c,1);
    bVar6 = (byte)local_1c;
  }
  if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
     ((*(byte *)(param_1 + 0x17d) != bVar6 &&
      (*(byte *)(param_1 + 0x17d) = bVar6, *(int *)(param_1 + 0x174) != 0)))) {
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
    (**(code **)(param_1 + 0x178))(param_1 + 0x16c,&local_1c);
  }
  if (local_21 < 5) {
    cVar10 = *(char *)(param_1 + 0x14c);
    if (cVar10 != '\0') {
      cVar10 = '\x01';
    }
    if ((*(char *)(param_1 + 0x14d) != cVar10) &&
       (*(char *)(param_1 + 0x14d) = cVar10, *(int *)(param_1 + 0x144) != 0)) {
      local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
      (**(code **)(param_1 + 0x148))(param_1 + 0x13c,&local_1c);
      goto LAB_08026dc0;
    }
LAB_08027216:
    cVar10 = *(char *)(param_1 + 0x134);
    if (cVar10 != '\0') {
      cVar10 = '\x01';
    }
    if ((*(char *)(param_1 + 0x135) != cVar10) &&
       (*(char *)(param_1 + 0x135) = cVar10, *(int *)(param_1 + 300) != 0)) {
      local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
      (**(code **)(param_1 + 0x130))(param_1 + 0x124,&local_1c);
      if (6 < local_21) goto LAB_08026dcc;
    }
LAB_0802724c:
    bVar11 = *(byte *)(param_1 + 0x164);
    if (2 < bVar11) {
      bVar11 = 3;
    }
    if ((*(byte *)(param_1 + 0x165) == bVar11) ||
       (*(byte *)(param_1 + 0x165) = bVar11, *(int *)(param_1 + 0x15c) == 0)) goto LAB_08027282;
    local_1c = (float)CONCAT31(local_1c._1_3_,bVar11);
    (**(code **)(param_1 + 0x160))(param_1 + 0x154,&local_1c);
    if (local_21 < 9) goto LAB_08027282;
LAB_08026dd2:
    puVar3 = (undefined4 *)param_2[1];
    local_20 = *(float *)(param_1 + 0x198);
    if (*(code **)*puVar3 == pcVar1) {
      pfVar5 = (float *)puVar3[2];
      pfVar9 = (float *)puVar3[3];
      if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
        software_bkpt(0);
        pfVar5 = (float *)puVar3[2];
        pfVar9 = (float *)puVar3[3];
      }
      local_20 = *pfVar9;
      puVar3[3] = pfVar9 + 1;
      if (pfVar5 < pfVar9 + 1) {
        software_bkpt(0);
      }
    }
    else {
      (**(code **)*puVar3)(puVar3,&local_20,4);
    }
    if ((((local_20 < *(float *)(param_1 + 0x19c) ==
           (NAN(local_20) || NAN(*(float *)(param_1 + 0x19c)))) &&
         (fVar13 = *(float *)(param_1 + 0x1a0),
         local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
        (local_20 != *(float *)(param_1 + 0x198))) &&
       (*(float *)(param_1 + 0x198) = local_20, *(int *)(param_1 + 0x18c) != 0)) {
      local_1c = local_20;
      (**(code **)(param_1 + 400))(param_1 + 0x184,&local_1c);
    }
LAB_08026e50:
    fVar13 = local_1c;
    if (9 < local_21) {
      puVar3 = (undefined4 *)param_2[1];
      bVar11 = *(byte *)(param_1 + 0x1b9);
      local_1c = (float)((uint)local_1c & 0xffffff00);
      if (*(code **)*puVar3 == pcVar1) {
        pbVar8 = (byte *)puVar3[2];
        pbVar7 = (byte *)puVar3[3];
        if (pbVar8 == pbVar7) {
          software_bkpt(0);
          pbVar8 = (byte *)puVar3[2];
          pbVar7 = (byte *)puVar3[3];
        }
        bVar6 = *pbVar7;
        local_1c._1_3_ = SUB43(fVar13,1);
        local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
        puVar3[3] = pbVar7 + 1;
        if (pbVar8 < pbVar7 + 1) {
          software_bkpt(0);
        }
      }
      else {
        (**(code **)*puVar3)(puVar3,&local_1c,1);
        bVar6 = (byte)local_1c;
      }
      if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
         ((*(byte *)(param_1 + 0x1b9) != bVar6 &&
          (*(byte *)(param_1 + 0x1b9) = bVar6, *(int *)(param_1 + 0x1b0) != 0)))) {
        local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
        (**(code **)(param_1 + 0x1b4))(param_1 + 0x1a8,&local_1c);
      }
      uVar2 = (uint)local_1c;
      puVar3 = (undefined4 *)param_2[1];
      bVar11 = *(byte *)(param_1 + 0x1d1);
      local_1c = (float)((uint)local_1c & 0xffffff00);
      if (*(code **)*puVar3 == pcVar1) {
        pbVar8 = (byte *)puVar3[2];
        pbVar7 = (byte *)puVar3[3];
        if (pbVar8 == pbVar7) {
          software_bkpt(0);
          pbVar8 = (byte *)puVar3[2];
          pbVar7 = (byte *)puVar3[3];
        }
        bVar6 = *pbVar7;
        local_1c._1_3_ = SUB43(uVar2,1);
        local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
        puVar3[3] = pbVar7 + 1;
        if (pbVar8 < pbVar7 + 1) {
          software_bkpt(0);
        }
      }
      else {
        (**(code **)*puVar3)(puVar3,&local_1c,1);
        bVar6 = (byte)local_1c;
      }
      if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
         ((*(byte *)(param_1 + 0x1d1) != bVar6 &&
          (*(byte *)(param_1 + 0x1d1) = bVar6, *(int *)(param_1 + 0x1c8) != 0)))) {
        local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
        (**(code **)(param_1 + 0x1cc))(param_1 + 0x1c0,&local_1c);
      }
      if (0xc < local_21) {
        FUN_08022d38(param_1 + 0x1d4,param_2);
        FUN_08022d38(param_1 + 0xbc4,param_2);
        if (0xd < local_21) {
          puVar3 = (undefined4 *)param_2[1];
          local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_000015c9)[param_1]);
          if (*(code **)*puVar3 == pcVar1) {
            pbVar8 = (byte *)puVar3[2];
            pbVar7 = (byte *)puVar3[3];
            if (pbVar8 == pbVar7) {
              software_bkpt(0);
              pbVar8 = (byte *)puVar3[2];
              pbVar7 = (byte *)puVar3[3];
            }
            bVar11 = *pbVar7;
            local_20 = (float)CONCAT31(local_20._1_3_,bVar11);
            puVar3[3] = pbVar7 + 1;
            if (pbVar8 < pbVar7 + 1) {
              software_bkpt(0);
            }
          }
          else {
            (**(code **)*puVar3)(puVar3,&local_20,1);
            bVar11 = (byte)local_20;
          }
          if (((((byte)(&DAT_000015ca)[param_1] <= bVar11) &&
               (bVar11 <= (byte)(&DAT_000015cb)[param_1])) && ((&DAT_000015c9)[param_1] != bVar11))
             && ((&DAT_000015c9)[param_1] = bVar11, *(int *)(&DAT_000015c0 + param_1) != 0)) {
            local_1c = (float)CONCAT31(local_1c._1_3_,bVar11);
            (**(code **)(&DAT_000015c4 + param_1))(&UNK_000015b8 + param_1,&local_1c);
          }
          fVar13 = local_1c;
          puVar3 = (undefined4 *)param_2[1];
          bVar11 = (&DAT_000015e1)[param_1];
          local_1c = (float)((uint)local_1c & 0xffffff00);
          if (*(code **)*puVar3 == pcVar1) {
            pbVar8 = (byte *)puVar3[2];
            pbVar7 = (byte *)puVar3[3];
            if (pbVar8 == pbVar7) {
              software_bkpt(0);
              pbVar8 = (byte *)puVar3[2];
              pbVar7 = (byte *)puVar3[3];
            }
            bVar6 = *pbVar7;
            local_1c._1_3_ = SUB43(fVar13,1);
            local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
            puVar3[3] = pbVar7 + 1;
            if (pbVar8 < pbVar7 + 1) {
              software_bkpt(0);
            }
          }
          else {
            (**(code **)*puVar3)(puVar3,&local_1c,1);
            bVar6 = (byte)local_1c;
          }
          if (((bVar6 < 2) || (bVar6 = bVar11, bVar11 < 2)) &&
             (((&DAT_000015e1)[param_1] != bVar6 &&
              ((&DAT_000015e1)[param_1] = bVar6, *(int *)(&DAT_000015d8 + param_1) != 0)))) {
            local_1c = (float)CONCAT31(local_1c._1_3_,bVar6);
            (**(code **)(&DAT_000015dc + param_1))(&UNK_000015d0 + param_1,&local_1c);
          }
          puVar3 = (undefined4 *)param_2[1];
          local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_000015f8)[param_1]);
          if (*(code **)*puVar3 == pcVar1) {
            pcVar12 = (char *)puVar3[2];
            pcVar4 = (char *)puVar3[3];
            if (pcVar12 == pcVar4) {
              software_bkpt(0);
              pcVar12 = (char *)puVar3[2];
              pcVar4 = (char *)puVar3[3];
            }
            cVar10 = *pcVar4;
            local_20 = (float)CONCAT31(local_20._1_3_,cVar10);
            puVar3[3] = pcVar4 + 1;
            if (pcVar12 < pcVar4 + 1) {
              software_bkpt(0);
            }
          }
          else {
            (**(code **)*puVar3)(puVar3,&local_20,1);
            cVar10 = (byte)local_20;
          }
          if (((&DAT_000015f8)[param_1] != cVar10) &&
             ((&DAT_000015f8)[param_1] = cVar10, *(int *)(&DAT_000015f0 + param_1) != 0)) {
            local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
            (**(code **)(&DAT_000015f4 + param_1))(&UNK_000015e8 + param_1,&local_1c);
          }
          puVar3 = (undefined4 *)param_2[1];
          local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00001610)[param_1]);
          if (*(code **)*puVar3 == pcVar1) {
            pcVar12 = (char *)puVar3[2];
            pcVar4 = (char *)puVar3[3];
            if (pcVar12 == pcVar4) {
              software_bkpt(0);
              pcVar12 = (char *)puVar3[2];
              pcVar4 = (char *)puVar3[3];
            }
            cVar10 = *pcVar4;
            local_20 = (float)CONCAT31(local_20._1_3_,cVar10);
            puVar3[3] = pcVar4 + 1;
            if (pcVar12 < pcVar4 + 1) {
              software_bkpt(0);
            }
          }
          else {
            (**(code **)*puVar3)(puVar3,&local_20,1);
            cVar10 = (byte)local_20;
          }
          if (((&DAT_00001610)[param_1] != cVar10) &&
             ((&DAT_00001610)[param_1] = cVar10, *(int *)(&DAT_00001608 + param_1) != 0)) {
            local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
            (**(code **)(&DAT_0000160c + param_1))(&UNK_00001600 + param_1,&local_1c);
          }
          puVar3 = (undefined4 *)param_2[1];
          local_20 = (float)CONCAT31(local_20._1_3_,(&DAT_00001628)[param_1]);
          if (*(code **)*puVar3 == pcVar1) {
            pcVar12 = (char *)puVar3[2];
            pcVar4 = (char *)puVar3[3];
            if (pcVar12 == pcVar4) {
              software_bkpt(0);
              pcVar12 = (char *)puVar3[2];
              pcVar4 = (char *)puVar3[3];
            }
            cVar10 = *pcVar4;
            local_20 = (float)CONCAT31(local_20._1_3_,cVar10);
            puVar3[3] = pcVar4 + 1;
            if (pcVar12 < pcVar4 + 1) {
              software_bkpt(0);
            }
          }
          else {
            (**(code **)*puVar3)(puVar3,&local_20,1);
            cVar10 = (byte)local_20;
          }
          if (((&DAT_00001628)[param_1] != cVar10) &&
             ((&DAT_00001628)[param_1] = cVar10, *(int *)(&DAT_00001620 + param_1) != 0)) {
            local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
            (**(code **)(&DAT_00001624 + param_1))(&UNK_00001618 + param_1,&local_1c);
          }
          if (0x10 < local_21) {
            puVar3 = (undefined4 *)param_2[1];
            local_20 = *(float *)(&DAT_00001644 + param_1);
            if (*(code **)*puVar3 == pcVar1) {
              pfVar5 = (float *)puVar3[2];
              pfVar9 = (float *)puVar3[3];
              if ((uint)((int)pfVar5 - (int)pfVar9) < 4) {
                software_bkpt(0);
                pfVar5 = (float *)puVar3[2];
                pfVar9 = (float *)puVar3[3];
              }
              local_20 = *pfVar9;
              puVar3[3] = pfVar9 + 1;
              if (pfVar5 < pfVar9 + 1) {
                software_bkpt(0);
              }
            }
            else {
              (**(code **)*puVar3)(puVar3,&local_20,4);
            }
            if ((((local_20 < *(float *)(&DAT_00001648 + param_1) ==
                   (NAN(local_20) || NAN(*(float *)(&DAT_00001648 + param_1)))) &&
                 (fVar13 = *(float *)(&DAT_0000164c + param_1),
                 local_20 == fVar13 || local_20 < fVar13 != (NAN(local_20) || NAN(fVar13)))) &&
                (local_20 != *(float *)(&DAT_00001644 + param_1))) &&
               (*(float *)(&DAT_00001644 + param_1) = local_20,
               *(int *)(&DAT_00001638 + param_1) != 0)) {
              local_1c = local_20;
              (**(code **)(&DAT_0000163c + param_1))(&UNK_00001630 + param_1,&local_1c);
            }
          }
        }
      }
      goto LAB_080272c0;
    }
LAB_080274fe:
    FUN_08009724(param_1 + 0x1d4);
    FUN_08009724(param_1 + 0xbc4);
  }
  else {
LAB_08026dc0:
    if (local_21 < 6) goto LAB_08027216;
    if (local_21 < 7) goto LAB_0802724c;
LAB_08026dcc:
    if (8 < local_21) goto LAB_08026dd2;
LAB_08027282:
    cVar10 = *(char *)(param_1 + 0x17c);
    if (cVar10 != '\0') {
      cVar10 = '\x01';
    }
    if ((*(char *)(param_1 + 0x17d) == cVar10) ||
       (*(char *)(param_1 + 0x17d) = cVar10, *(int *)(param_1 + 0x174) == 0)) goto LAB_08026e50;
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
    (**(code **)(param_1 + 0x178))(param_1 + 0x16c,&local_1c);
    if (8 < local_21) goto LAB_08026dd2;
LAB_080272c0:
    if (local_21 < 10) goto LAB_080274fe;
  }
  if (local_21 < 0xf) {
    fVar13 = *(float *)(param_1 + 0x4c);
    if (*(float *)(param_1 + 0x44) < fVar13 == (NAN(*(float *)(param_1 + 0x44)) || NAN(fVar13))) {
      coprocessor_function2(10,8,3,in_cr4,in_cr3,in_cr3);
    }
    if ((fVar13 == *(float *)(param_1 + 0x48)) ||
       (*(float *)(param_1 + 0x48) = fVar13, *(int *)(param_1 + 0x3c) == 0)) goto LAB_08027542;
    local_1c = fVar13;
    (**(code **)(param_1 + 0x40))(param_1 + 0x34,&local_1c);
  }
  if (0xf < local_21) {
    return;
  }
LAB_08027542:
  cVar10 = (&DAT_000015e0)[param_1];
  if (cVar10 != '\0') {
    cVar10 = '\x01';
  }
  if (((&DAT_000015e1)[param_1] != cVar10) &&
     ((&DAT_000015e1)[param_1] = cVar10, *(int *)(&DAT_000015d8 + param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,cVar10);
    (**(code **)(&DAT_000015dc + param_1))(&UNK_000015d0 + param_1,&local_1c);
  }
  if ((((7 < local_21) && (*(char *)(param_1 + 0x165) == '\0')) &&
      ((&DAT_000015e1)[param_1] != '\x01')) &&
     ((&DAT_000015e1)[param_1] = 1, *(int *)(&DAT_000015d8 + param_1) != 0)) {
    local_1c = (float)CONCAT31(local_1c._1_3_,1);
    (**(code **)(&DAT_000015dc + param_1))(&UNK_000015d0 + param_1,&local_1c);
  }
  local_1c = *(float *)(param_1 + 0xf4);
  if (*(float *)(param_1 + 0xcc) < local_1c == (NAN(*(float *)(param_1 + 0xcc)) || NAN(local_1c))) {
    coprocessor_function2(10,8,3,in_cr6,in_cr5,in_cr5);
  }
  if ((local_1c != *(float *)(param_1 + 0xf0)) &&
     (*(float *)(param_1 + 0xf0) = local_1c, *(int *)(param_1 + 0xe4) != 0)) {
    (**(code **)(param_1 + 0xe8))(param_1 + 0xdc,&local_1c);
    return;
  }
  return;
}


```

### callee `FUN_08009bcc` @ `08009bcc`
```c

void FUN_08009bcc(undefined4 param_1)

{
  undefined4 local_c [3];
  
  local_c[0] = 0x11;
  FUN_08009738(param_1,local_c);
  return;
}


```
