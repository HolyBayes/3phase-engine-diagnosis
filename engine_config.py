# This Python file uses the following encoding: latin-1
config = {
    "f1": 50, # основная частота питания 50 Гц
    "f_sampling": 10000, # частота дискретизации 10 кГц
    "s": 0.028, # скольжение двигателя 2.8% (справочное), 2.67% (расчётное)
    "R_s": 34, # число пазов (стержней) ротора
    "p": 2, # число пар полюсов,
    "f_r": 1460/60, # частота вращения ротора (вала) 1460 RPM
    "n": 8, # число шариков в подшипнике
    "beta": 0, # угол контакта
    "D_pit": 65, # диаметр окружности центра шариков (мм)
    "D_ball": 15.0810 # диаметр шарика (мм)
}
