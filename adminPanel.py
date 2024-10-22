from adminPanelMethods import adminControl
import asyncio


async def main():
    while True:
        move = await asyncio.to_thread(input, "Введите команду: ")
        if move == "change mask":
            mask_method = await asyncio.to_thread(input, "Введите тип маски: ")
            await adminControl.changeMaskMethod(int(mask_method))

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())
