# ==========================
# Подготовка окружения
library(here)

source(here("r", "set_env.r"), encoding = "UTF-8")

# Пути к данным
PROJECT_ROOT <- here::here()
path_to_data <- file.path(PROJECT_ROOT, "data", "final", "votes.xlsx")
path_to_results <- file.path(PROJECT_ROOT, "bmodels", "fitted")

# Чтение и предобработка данных
df <- read_excel(path_to_data)

marpor <- df %>%
  select(
    support = share_yes_votes,
    country,
    rile,
    gov = gov_opp_num,
    wthdr = withdrawal_or_anti_interventionvote,
    alliance = membership_alliance,
    postcom = post_communist,
    pervote,
    herf = herfgov,
    un,
    nato,
    eu,
    combat,
    cooperative,
    humanitarian
  ) %>%
  na.omit() %>%
  mutate(
    rile = rescale(rile, to = c(0, 10), from = c(-100, 100)),
    gov = as.logical(gov),
    wthdr = as.logical(wthdr),
    alliance = as.logical(alliance),
    postcom = as.logical(postcom),
    un = as.logical(un),
    nato = as.logical(nato),
    eu = as.logical(eu),
    combat = as.logical(combat),
    cooperative = as.logical(cooperative),
    humanitarian = as.logical(humanitarian)
  )

glimpse(marpor)

# Обучение модели 1
zoib_gov <- bf(
  support ~ rile*gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  phi ~ rile*gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  zoi ~ rile*gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  coi ~ rile*gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf
)

zoib_gov <- brm(
  zoib_gov,
  data = marpor,
  family = zero_one_inflated_beta(),
  init = 0,
  control = list(adapt_delta = 0.97, max_treedepth = 12)
)

# Сохраняем результаты
saveRDS(zoib_gov, file = file.path(path_to_results, "zoib_gov.rds"))

message("✅ Model trained and saved at: ", file.path(path_to_results, "zoib_gov.rds"))

# Обучение модели 2
combat <- bf(
  support ~ rile*combat + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  phi ~ rile*combat + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  zoi ~ rile*combat + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  coi ~ rile*combat + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf
)

zoib_combat <- brm(
  combat,
  data = marpor, 
  family = zero_one_inflated_beta(),
  init = 0,
  control = list(adapt_delta = 0.97, max_treedepth = 12))

# Сохраняем результаты
saveRDS(zoib_combat, file = file.path(path_to_results, "zoib_combat.rds"))

message("✅ Model trained and saved at: ", file.path(path_to_results, "zoib_combat.rds"))

# Обучение модели 3
cooperative <- bf(
  support ~ rile*cooperative + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  phi ~ rile*cooperative + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  zoi ~ rile*cooperative + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  coi ~ rile*cooperative + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf
)

zoib_cooperative <- brm(
  cooperative,
  data = marpor, 
  family = zero_one_inflated_beta(),
  init = 0,
  control = list(adapt_delta = 0.97, max_treedepth = 12))

# Сохраняем результаты
saveRDS(zoib_cooperative, file = file.path(path_to_results, "zoib_cooperative.rds"))

message("✅ Model trained and saved at: ", file.path(path_to_results, "zoib_cooperative.rds"))

# Обучение модели 4
humanitarian <- bf(
  support ~ rile*humanitarian + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  phi ~ rile*humanitarian + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  zoi ~ rile*humanitarian + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf,
  coi ~ rile*humanitarian + gov + alliance + wthdr + postcom + un + nato + eu + pervote + herf
)

zoib_humanitarian <- brm(
  humanitarian,
  data = marpor, 
  family = zero_one_inflated_beta(),
  init = 0,
  control = list(adapt_delta = 0.97, max_treedepth = 12))

# Сохраняем результаты
saveRDS(zoib_humanitarian, file = file.path(path_to_results, "zoib_humanitarian.rds"))

message("✅ Model trained and saved at: ", file.path(path_to_results, "zoib_humanitarian.rds"))