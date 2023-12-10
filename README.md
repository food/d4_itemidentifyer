# TODO
## Load data from https://mobalytics.gg/
https://mobalytics.gg/builds-widget-documentation/

https://mobalytics.gg/api-diablo4/v2/graphql/query
PAYLOAD:
{"operationName":"Diablo4MetaBuildPageQuery","variables":{"filter":{"id":"ball-lightning-mana-tank"}},"query":"query Diablo4MetaBuildPageQuery($filter: Diablo4MetaBuildFilter!) {\n  diablo4 {\n    pages {\n      buildPage {\n        __typename\n        ... on Diablo4BuildPage {\n          metadata {\n            ...PageMetaFragment\n            __typename\n          }\n          communityBuildsText\n          communityBuildsLink {\n            __typename\n            ... on Diablo4Link {\n              linkText\n              linkUrl\n              __typename\n            }\n          }\n          __typename\n        }\n      }\n      __typename\n    }\n    game {\n      settings {\n        __typename\n        ... on Diablo4GenericError {\n          message\n          __typename\n        }\n        ... on Diablo4GameSettings {\n          skillLimit\n          paragonNodesLimit\n          currentSeason {\n            __typename\n            ...BuildSeasonFragment\n          }\n          __typename\n        }\n      }\n      metaBuild(filter: $filter) {\n        __typename\n        ... on Diablo4GenericError {\n          message\n          __typename\n        }\n        ... on Diablo4MetaBuild {\n          class {\n            __typename\n            ... on Diablo4Class {\n              id\n              name\n              iconUrl\n              backgroundImageUrl\n              __typename\n            }\n          }\n          types {\n            __typename\n            ... on Diablo4BuildType {\n              id\n              name\n              __typename\n            }\n          }\n          season {\n            __typename\n            ...BuildSeasonFragment\n          }\n          tier {\n            __typename\n            ...TierFragment\n          }\n          build {\n            __typename\n            ... on Diablo4CustomBuildV2 {\n              ...CustomBuildDataByIdBuildFragment\n              __typename\n            }\n          }\n          __typename\n        }\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BuildSeasonFragment on Diablo4Season {\n  id\n  name\n  startingAt\n  seasonMechanics\n  __typename\n}\n\nfragment TierFragment on Diablo4Tier {\n  ... on Diablo4Tier {\n    id\n    name\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment PageMetaFragment on Diablo4SeoMetaData {\n  title\n  ogImage\n  description\n  keywords\n  __typename\n}\n\nfragment CustomBuildDataByIdBuildFragment on Diablo4CustomBuildV2 {\n  id\n  name\n  updatedAt\n  isFavourite\n  favouriteCounter\n  isPublished\n  links {\n    linkText\n    linkType\n    linkUrl\n    __typename\n  }\n  class {\n    __typename\n    id\n    name\n    iconUrl\n    backgroundImageUrl\n  }\n  assignedSkills {\n    __typename\n    ... on Diablo4AssignedSkill {\n      position\n      skill {\n        id\n        name\n        iconUrl\n        type {\n          __typename\n          ... on Diablo4SkillType {\n            id\n            name\n            __typename\n          }\n          ... on Diablo4GenericError {\n            message\n            __typename\n          }\n        }\n        __typename\n      }\n      __typename\n    }\n  }\n  assignedVampirePowers {\n    __typename\n    ... on Diablo4AssignedVampirePower {\n      position\n      vampirePower {\n        id\n        name\n        iconUrl\n        description\n        pact {\n          divinity\n          eternity\n          ferocity\n          __typename\n        }\n        type\n        __typename\n      }\n      __typename\n    }\n  }\n  paragonNodes {\n    id\n    __typename\n  }\n  paragonBoards {\n    x\n    y\n    rotation\n    board {\n      id\n      __typename\n    }\n    glyph {\n      id\n      __typename\n    }\n    __typename\n  }\n  skills {\n    actionType\n    skill {\n      id\n      __typename\n    }\n    __typename\n  }\n  expertise {\n    id\n    __typename\n  }\n  summons {\n    type\n    upgrade\n    spec {\n      id\n      __typename\n    }\n    __typename\n  }\n  boons {\n    type\n    value {\n      id\n      __typename\n    }\n    __typename\n  }\n  specialization {\n    id\n    __typename\n  }\n  enchantments {\n    id\n    __typename\n  }\n  gear {\n    slot {\n      id\n      __typename\n    }\n    aspect {\n      id\n      __typename\n    }\n    item {\n      id\n      __typename\n    }\n    stats {\n      __typename\n      ... on Diablo4AffixStat {\n        id\n        __typename\n      }\n    }\n    __typename\n  }\n  gems {\n    gem {\n      id\n      __typename\n    }\n    slot {\n      id\n      __typename\n    }\n    __typename\n  }\n  hearts {\n    heart {\n      id\n      __typename\n    }\n    slot {\n      id\n      __typename\n    }\n    __typename\n  }\n  gameplayLoop\n  buildOverview\n  buildSummary\n  season {\n    __typename\n    ...BuildSeasonFragment\n  }\n  author {\n    __typename\n    ...CustomBuildAuthorFragment\n  }\n  inDepthExplanation {\n    ... on Diablo4InDepthExplanationBlock {\n      title\n      content\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CustomBuildAuthorFragment on Diablo4CustomAuthor {\n  id\n  name\n  socialLinks: links {\n    __typename\n    ... on Diablo4AuthorLink {\n      link: url\n      type: network {\n        __typename\n        ... on Diablo4SocialLinkType {\n          id\n          name\n          iconUrl\n          __typename\n        }\n      }\n      __typename\n    }\n  }\n  __typename\n}\n"}

Response:
data.diablo4.game.metaBuild.build.gear(.stats)
data.diablo4.game.metaBuild.build.gear.slot.id = ring-1

## Item Power needs to be bigger then used item

## Wapon needs to be checkt the whole list for one hand or two hand and attributes // get from internal list
## offhand needs to be checkt the whole list for attributes // get from internal list
https://diablo4.wiki.fextralife.com/Weapons


Barbarian
Mainhand: 1 Handed Axe, 2 Handed Axe, 1 Handed Sword, 2 Handed Sword, 1 Handed Mace, 2 Handed Mace, Polearm, 
Offhand: 1 Handed Axe, 1 Handed Sword, 1 Handed Mace, 

Druid
Mainhand: 1 Handed Axe, 2 Handed Axe, 1 Handed Mace, 2 Handed Mace, Staff, 2 Handed Staff,
Offhand:

Necromancer
Mainhand: 1 Handed Sword, 2 Handed Sword, 1 Handed Scythe, 2 Handed Scythe, Staff, 2 Handed Staff,
Offhand: Wand, Shield, Focus

Rogue
Mainhand: 1 Handed Sword, Dagger, Bow, Crossbow, 
Offhand: 1 Handed Sword, Dagger,

Sorcerer
Mainhand: Dagger, Staff, 2 Handed Staff,
Offhand: Wand, Focus

2-Hand Mace
2-Hand Sword

## Aspects on legendaries

# O and OO in name is not nice to parse cause d4 font