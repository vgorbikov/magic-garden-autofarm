import asyncio
from asyncio import tasks
from game.state import GameState
from game.commands import CommandProvider, PurchaseShopItem
from config import Config


class Bot():
    def __init__(self, conf: Config, game_state: GameState, command_provider: CommandProvider):
        self.game_state: GameState = game_state
        self.command_provider: CommandProvider = command_provider
        self.config: Config = conf

    async def shop_items_directive(self):
        print('<i> Shop items directive running...')
        for target in self.config.directives.shop_items.targets:
            target_shop_filter = [s for s in self.game_state.shops if target.shop==s.shopName]
            if len(target_shop_filter)==0:
                print(f'\tNot found shop {target.shop.value}')
                continue 
            target_shop = target_shop_filter[0]
            target_item_filter = [i for i in target_shop.inventory if i.itemUName==target.item]
            if len(target_item_filter)==0:
                print(f'\tNot found item {target.item.value} in {target_shop.shopName.value}')
                continue
            target_item = target_item_filter[0]
            if target_item.currentUserStock == 0:
                print(f'\t{target_item.itemUName.value} isn`t available (stock=0)')
                continue
            print(f'\tTry to buy {target_item.currentUserStock} {target_item.itemUName.value}:')
            for i in range(10):
                purchase_command = PurchaseShopItem(
                    shop=target.shop,
                    itemType=target_item.itemType,
                    item=target.item,
                    count=target_item.currentUserStock
                )
                result = await self.command_provider.execute(purchase_command)
                if result.ok:
                    print(f'\t\t[{i}] Success!')
                    break
                else:
                    print(f'\t\t[{i}] Fail: {result.code}')
                    await asyncio.sleep(0.2)
            await asyncio.sleep(1)
        await asyncio.sleep(60)


    async def run_directive_loop(self):
        print('<i> Directive loop is running')
        while True:
            if not self.game_state.is_ready.is_set():
                await self.game_state.is_ready.wait()
            if not self.command_provider.is_ready.is_set():
                await self.command_provider.is_ready.wait()
            print('-'*30)
            print(f'<i> Directive loop iteration starts...')
            if self.config.directives.shop_items.status:
                shop_items_tasks = asyncio.create_task(self.shop_items_directive())
                print('<i> Shop items directive planned')
            await shop_items_tasks
