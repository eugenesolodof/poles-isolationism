# ==========================
# Установка и загрузка необходимых пакетов

packages <- c(
  "tidyverse", "dplyr", "readxl", "scales",
  "brms", "rstan", "loo", "posterior", "here"
)

options(repos = c(CRAN = "https://cloud.r-project.org"))

installed <- rownames(installed.packages())

for(pkg in packages){
  if(!(pkg %in% installed)){
    message("Installing package: ", pkg)
    tryCatch(
      install.packages(pkg, type = "source"),
      error = function(e) message("Failed to install ", pkg, ":\n", e)
    )
  }
}

lapply(packages, function(pkg){
  message("Loading package: ", pkg)
  suppressPackageStartupMessages(library(pkg, character.only = TRUE))
})

# Создаём папку для результатов (если нет)
PROJECT_ROOT <- here::here()
dir.create(file.path(PROJECT_ROOT, "bmodels", "fitted"), recursive = TRUE, showWarnings = FALSE)

message("✅ Environment ready.")