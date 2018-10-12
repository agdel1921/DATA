install.packages('ggplot2')
install.packages('dplyr')
install.packages('fortunes')
install.packages("rio")
install_formats()
install.packages('modules')
library("datasets")
load.libraries <- c('data.table', 'testthat', 'gridExtra', 'corrplot', 'GGally', 'ggplot2', 'e1071', 'dplyr', 'rio', 'modules')
library("rio")
readRDS(file = "D:/NTUC/raw_data/rds_source/transaction.rds")
y <- import("D:/NTUC/raw_data/rds_source/transaction.rds")

readRDS(file = "D:/NTUC/raw_data/rds_source/agent.rds")
x <- import("D:/NTUC/raw_data/rds_source/agent.rds")


readRDS(file = "D:/NTUC/raw_data/Data_set2/NewData/customer.rds")
z <- import("D:/NTUC/raw_data/rds_source/customer.rds")



readRDS(file = "D:/NTUC/raw_data/rds_source/product.rds")
a <- import("D:/NTUC/raw_data/rds_source/product.rds")


readRDS(file = "D:/NTUC/raw_data/rds_source/houseview_latize.rds")
a1 <- import("D:/NTUC/raw_data/rds_source/houseview_latize.rds")



readRDS(file = "D:/NTUC/raw_data/rds_source/House_View/customerview_latize.rds")
a2 <- import("D:/NTUC/raw_data/rds_source/House_View/customerview_latize.rds")


readRDS(file = "D:/NTUC/raw_data/rds_source/House_View/relation_latize.rds")
a3 <- import("D:/NTUC/raw_data/rds_source/House_View/relation_latize.rds")



#names(y)
d#im(y)
#str(y)
#head(y, n=10)
#tail(y, n=5)
#splt <- split(y,rep(1:60,each=300000))

# Writing files in the csv
write.csv(y,"transaction.csv")

write.csv(x,"agent.csv")

write.csv(z,"customer.csv")

write.csv(a,"product.csv")

write.csv(a1,"houseview.csv")

write.csv(a2,"customer_view.csv")
write.csv(a3,"relation_houseview.csv")

