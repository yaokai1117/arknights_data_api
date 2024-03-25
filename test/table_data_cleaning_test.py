import unittest

from data_processing.table_data_cleaning import process_table_data


class TestStringMethods(unittest.TestCase):

    def test_remove_tags(self):
        data = {
            'description': '立即获得<@ba.vup>+12</>点部署费用，攻击力增加<@ba.vup>+80%</>。',
        }
        process_table_data(data)
        self.assertEqual(data['description'], '立即获得+12点部署费用，攻击力增加+80%。')

    def test_remove_nested_tags(self):
        data = {
            'description': '立即获得<@ba.vup>+<@ba.vap>12</></>点部署费用，攻击力增加<@ba.vup>+80%</>。',
        }
        process_table_data(data)
        self.assertEqual(data['description'], '立即获得+12点部署费用，攻击力增加+80%。')

    def test_interolate_integer(self):
        data = {
            'description': '攻击变为随机对攻击范围内至多{attack@max_target}个敌人发射熔岩。',
            "blackboard": [
                {
                    "key": "attack@max_target",
                    "value": 3.0,
                    "valueStr": None
                }
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '攻击变为随机对攻击范围内至多3个敌人发射熔岩。')

    def test_interolate_negative_integer(self):
        data = {
            'description': '所有命中目标在10秒内防御力-{-def}',
            "blackboard": [
                {
                    "key": "def",
                    "value": -330.0,
                    "valueStr": None
                },
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '所有命中目标在10秒内防御力-330')

    def test_interpolate_integer_explicitly(self):
        data = {
            'description': '第二天赋的效果提升至{talent_scale:0}倍',
            "blackboard": [
                {
                    "key": "talent_scale",
                    "value": 3.0,
                    "valueStr": None
                },
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '第二天赋的效果提升至3倍')

    def test_interpolate_float_first_decimal_place(self):
        data = {
            'description': '使命中目标晕眩{attack@stun:0.0}秒',
            "blackboard": [
                {
                    "key": "attack@stun",
                    "value": 1.0,
                    "valueStr": None
                }
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '使命中目标晕眩1.0秒')

    def test_interolate_percentage(self):
        data = {
            'description': '攻击力+{atk:0%}',
            "blackboard": [
                {
                    "key": "atk",
                    "value": 1.3,
                    "valueStr": None
                },
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '攻击力+130%')

    def test_interolate_percentage_first_decimal_place(self):
        data = {
            'description': '每秒恢复最大生命的{HP_RECOVERY_PER_SEC_BY_MAX_HP_RATIO:0.0%}',
            "blackboard": [
                {
                    "key": "hp_recovery_per_sec_by_max_hp_ratio",
                    "value": 0.045,
                    "valueStr": None
                }
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '每秒恢复最大生命的4.5%')

    def test_interolate_with_special_characters(self):
        data = {
            'description': '攻击力+{reed2_skil_3[switch_mode].atk:0%} 技能期间附带灼痕效果的敌人每秒受到{talent@s3_atk_scale:0%}焰影苇草攻击力的法术伤害',
            "blackboard": [
                {
                    "key": "talent@s3_atk_scale",
                    "value": 0.4,
                    "valueStr": None
                },
                {
                    "key": "reed2_skil_3[switch_mode].atk",
                    "value": 0.45,
                    "valueStr": None
                },
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '攻击力+45% 技能期间附带灼痕效果的敌人每秒受到40%焰影苇草攻击力的法术伤害')

    def test_remove_tage_and_interpolate(self):
        data = {
            'description': '使命中目标<$ba.stun>晕眩</><@ba.vup>{attack@stun:0.0}</>秒',
            "blackboard": [
                {
                    "key": "attack@stun",
                    "value": 1.0,
                    "valueStr": None
                }
            ]
        }
        process_table_data(data)
        self.assertEqual(data['description'], '使命中目标晕眩1.0秒')


if __name__ == '__main__':
    unittest.main()
