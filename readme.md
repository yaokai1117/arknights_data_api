## arknights-data-api

A [GraphQL](https://graphql.org/) interface for [Arknights game data](https://github.com/Kengxxiao/ArknightsGameData).  **Everyting is still WIP.**

**Note**: currently only support Chinese version data set.  

The code contains two parts: one script to periodically check the Arknights game data github for updates and store them into MongoDB, another one to start a GraphQL server for querying those data.

The full schema can be found in [schema.graphql](https://github.com/yaokai1117/arknights_data_api/blob/main/graphql_api/schema.graphql) file.


## Example query 1 - Basic info about a character: 
```
{
  characters(filter: {tagList: ["治疗", "防护", "输出"], rarity: 6}) {
    characterPrefabKey
    name
    description
    position
    profession
    subProfession
    traits
    talents
    skills {
    	skillName
    }
    phases {
      attributesKeyFrames {
        level
        maxHp
        atk
      }
      maxLevel
    }
    potentialRanks
  }
}
```

Results: 

<details>
  <summary>Click me to expand</summary>

```js
  {
  "data": {
    "characters": [
      {
        "characterPrefabKey": "char_423_blemsh",
        "name": "瑕光",
        "description": "卡西米尔骑士瑕光，即将成熟的荣光。\n如果找不到她，请去询问工程部干员。",
        "position": "MELEE",
        "profession": "TANK",
        "subProfession": "guardian",
        "traits": "技能可以治疗友方单位",
        "talents": [
          "剑盾骑士: 在场时所有受击回复的技能在干员攻击时也回复1点技力",
          "仁慈: 自身可以攻击并优先攻击沉睡的目标且攻击力提升至144%（+4%）"
        ],
        "skills": [
          {
            "skillName": "光芒涌动"
          },
          {
            "skillName": "慑敌辉光"
          },
          {
            "skillName": "先贤化身"
          }
        ],
        "phases": [
          {
            "attributesKeyFrames": [
              {
                "level": 1,
                "maxHp": 1346,
                "atk": 207
              },
              {
                "level": 50,
                "maxHp": 1820,
                "atk": 297
              }
            ],
            "maxLevel": 50
          },
          {
            "attributesKeyFrames": [
              {
                "level": 1,
                "maxHp": 1820,
                "atk": 297
              },
              {
                "level": 80,
                "maxHp": 2334,
                "atk": 402
              }
            ],
            "maxLevel": 80
          },
          {
            "attributesKeyFrames": [
              {
                "level": 1,
                "maxHp": 2334,
                "atk": 402
              },
              {
                "level": 90,
                "maxHp": 3242,
                "atk": 491
              }
            ],
            "maxLevel": 90
          }
        ],
        "potentialRanks": [
          "部署费用-1",
          "再部署时间-4秒",
          "攻击力+26",
          "第二天赋效果增强",
          "部署费用-1"
        ]
      }
    ]
  }
}
```

</details>

## Example query 2 - Basic info about a skill (and also joint with its character): 
```
{
  skill(filter: {skillName: "先贤化身"}) {
    skillId
    skillName
    characters {
      characterPrefabKey
      name
      description
      tagList
      position
    }
    levels {
      description
      skillType
      durationType
      duration
      spType
      spCost
      initialSp
      maxCharge
    }
  }
}
```

Results: 

<details>
  <summary>Click me to expand</summary>

```js
  {
  "data": {
    "skill": {
      "skillId": "skchr_blemsh_3",
      "skillName": "先贤化身",
      "characters": [
        {
          "characterPrefabKey": "char_423_blemsh",
          "name": "瑕光",
          "description": "卡西米尔骑士瑕光，即将成熟的荣光。\n如果找不到她，请去询问工程部干员。",
          "tagList": [
            "防护",
            "治疗",
            "输出"
          ],
          "position": "MELEE"
        }
      ],
      "levels": [
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 20,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 30,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 21,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 30,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 22,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 30,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 23,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 29,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 24,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 29,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 25,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 29,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 26,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 28,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 27,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 27,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 28,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 26,
          "initialSp": 15,
          "maxCharge": 1
        },
        {
          "description": "攻击力+{atk:0%}，防御力+{def:0%}，每次攻击额外造成相当于攻击力{attack@blemsh_s_3_extra_dmg[magic].atk_scale:0%}的法术伤害，并恢复周围一名其他友方单位相当于攻击力{heal_scale:0%}的生命",
          "skillType": "MANUAL",
          "durationType": "NONE",
          "duration": 30,
          "spType": "INCREASE_WHEN_TAKEN_DAMAGE",
          "spCost": 25,
          "initialSp": 15,
          "maxCharge": 1
        }
      ]
    }
  }
}
```

</details>

## Example query 3 - the proficient (专精) material needed for a skill: 
```
{
  skill(filter: {skillName: "先贤化身"}) {
    skillId
    skillName
    skillRequirements {
      character {
				name
      }
      proficientRequirements {
        timeCost
        materialCost {
          count
          id
        }
      }
    }
  }
}
```

Results: 

<details>
  <summary>Click me to expand</summary>

```js
  {
  "data": {
    "skill": {
      "skillId": "skchr_blemsh_3",
      "skillName": "先贤化身",
      "skillRequirements": [
        {
          "character": {
            "name": "瑕光"
          },
          "proficientRequirements": [
            {
              "timeCost": 28800,
              "materialCost": [
                {
                  "count": 8,
                  "id": "3303"
                },
                {
                  "count": 4,
                  "id": "31014"
                },
                {
                  "count": 11,
                  "id": "30013"
                }
              ]
            },
            {
              "timeCost": 57600,
              "materialCost": [
                {
                  "count": 12,
                  "id": "3303"
                },
                {
                  "count": 4,
                  "id": "30104"
                },
                {
                  "count": 7,
                  "id": "30084"
                }
              ]
            },
            {
              "timeCost": 86400,
              "materialCost": [
                {
                  "count": 15,
                  "id": "3303"
                },
                {
                  "count": 6,
                  "id": "30125"
                },
                {
                  "count": 5,
                  "id": "31024"
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

</details>
