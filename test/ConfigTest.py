from src.Config import Config

config = Config()
config.reload()

temp = config.get_temp()

print temp
print config.get_day()