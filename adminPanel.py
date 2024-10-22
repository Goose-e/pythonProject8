from adminPanelMethods import adminControl
import asyncio
from enumMask import Mask

class AdminPanel:

    def __init__(self):
        self.r = 0  # Инициализация атрибута r

    async def main(self):
        while True:
            move = await asyncio.to_thread(input, "Введите команду: ")
            if move == "change mask":
                mask_method = await asyncio.to_thread(input, "Введите тип маски: ")
                self.r = int(mask_method)  # Изменяем значение r через атрибут класса
                selected_mask = await self.maskSw(self.r)
                print(selected_mask)
                if selected_mask:
                    await adminControl.changeMaskMethod(selected_mask)
                else:
                    print("Неверный тип маски. Попробуйте снова.")

    async def maskSw(self, num):
        mask_switch = {
            1: Mask.maskType,
            2: Mask.maskType2,
            3: Mask.maskType3,
        }
        selected_mask = mask_switch.get(num, Mask.maskType)
        return selected_mask


# Запуск основной функции
if __name__ == "__main__":
    admin_panel = AdminPanel()  # Создаем экземпляр AdminPanel
    asyncio.run(admin_panel.main())  # Запускаем метод main
