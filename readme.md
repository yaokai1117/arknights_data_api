## arknights-data-api

A [GraphQL](https://graphql.org/) interface for [Arknights game data](https://github.com/Kengxxiao/ArknightsGameData).  **Everyting is still WIP.**

**Note**: currently only support Chinese version data set.  

The code contains two parts: one script to periodically check the Arknights game data github for updates and store them into MongoDB, another one to start a GraphQL server for querying those data.

The full schema can be found in [schema.graphql](https://github.com/yaokai1117/arknights_data_api/blob/main/graphql_api/schema.graphql) file.


## Example query 1 - Basic info about a character: 
```
{
  characters(filter: {tagList: ["治疗", "防护", "输出"], rarity: 6}) {
    name
    description
    position
    profession
    subProfession
    traits
    talents
    skills(index: null) {
    	skillName
    }
    phases(index: -1) {
      attributesKeyFrames(index: -1) {
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
    skillName
    characters {
      name
      description
      tagList
      position
    }
    levels(index: -1) {
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
      "skillName": "先贤化身",
      "characters": [
        {
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
          "description": "攻击力+110%，防御力+60%，每次攻击额外造成相当于攻击力100%的法术伤害，并恢复周围一名其他友方单位相当于攻击力100%的生命",
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
    skillName
    skillRequirements {
      character {
	  name
      }
      proficientRequirements {
        timeCost
        materialCost {
          count
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
