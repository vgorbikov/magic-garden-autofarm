import asyncio
from typing import Optional, Tuple

from bot.directives.bot_directive import BotDirective
from game.commands import PurchaseShopItem
from game.game_types import ToolId, Species, EggId, Shops, Unknown



class ShopItemsDirecrtive(BotDirective):

    async def _directive_loop(self):
        while True:
            if not self.is_working.is_set():
                break 
            print('[/item_shoping] directive running...')
            for target in self.config.directives.shop_items.targets:
                target_item_in_player_inventory_filter = [i for i in self.game_state.currentPlayer.inventory if i.itemUName==target.item]
                target_item_in_player_storages_filter = [i for s in self.game_state.currentPlayer.storages for i in s.items if i.itemUName==target.item]
                await asyncio.sleep(0.1)
                total_count = sum([i.quantity for i in target_item_in_player_inventory_filter] + [i.quantity for i in target_item_in_player_storages_filter])
                await asyncio.sleep(0.1)
                if target.item_limit:
                    if total_count >= target.item_limit:
                        continue
                target_shop_filter = [s for s in self.game_state.shops if target.shop==s.shopName]
                await asyncio.sleep(0.1)
                target_shop = target_shop_filter[0]
                if target_shop.restockId is None:
                    continue 
                target_item_filter = [i for i in target_shop.inventory if i.itemUName==target.item]
                await asyncio.sleep(0.1)
                target_item = target_item_filter[0]
                if target_item.currentUserStock == 0:
                    continue
                print(f'[/item_shoping] {target_item.itemUName.value} [{total_count}/{target.item_limit}] - try to buy another {target_item.currentUserStock}')
                for i in range(10):
                    purchase_command = PurchaseShopItem(
                        shop=target.shop,
                        itemType=target_item.itemType,
                        item=target.item,
                        count=target_item.currentUserStock
                    )
                    result = await self.command_provider.execute(purchase_command)
                    if result.ok:
                        print(f'[/item_shoping]\t[{i}] Success buy {target_item.currentUserStock} {target_item.itemUName.value}!')
                        break
                    else:
                        print(f'[/item_shoping]\t[{i}] Fail buy {target_item.currentUserStock} {target_item.itemUName.value}: {result.code}')
                        await asyncio.sleep(0.2)
                await asyncio.sleep(0.5)
            await asyncio.sleep(60)


    def ok(self) -> Tuple[bool, Optional[str]]:
        directive_settings = self.config.directives.shop_items
        for target_no in range(len(directive_settings.targets)):
            target = directive_settings.targets[target_no]
            if target.shop == Shops.UNKNOWN:
                return False, f'Target {target_no} invalid. Shop is unknown.'
            if target.item in (ToolId.UNKNOWN, EggId.UNKNOWN, Species.UNKNOWN, Unknown.UNKNOWN):
                return False, f'Target {target_no} invalid. Item name unknown.'
        return True, None
