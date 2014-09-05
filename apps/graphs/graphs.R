library(extrafont)
loadfonts(quiet=T)

eval_graph = function(){
  eval = read.csv("~/Projects/storyline/apps/graphs/csv/eval_table.csv", header=F)
  names(eval) = c("story", "question", "Nenhum/Outro", "Sim", "N\u00E3o")
  
  eval_has_read = eval[eval$question == "has_read",]
  eval_has_context = eval[eval$question == "has_context",]
  eval_has_gap = eval[eval$question == "has_gap",]
  eval_has_similar = eval[eval$question == "has_similar",]
  
  has_read = eval_has_read[,-1:-2]
  rownames(has_read) = eval_has_read$story
  
  has_context = eval_has_context[,-1:-2]
  rownames(has_context) = eval_has_context$story
  
  has_gap = eval_has_gap[,-1:-2]
  rownames(has_gap) = eval_has_gap$story
  
  has_similar = eval_has_similar[,-1:-2]
  rownames(has_similar) = eval_has_similar$story
  
#   par(mar = c(5.1, 4.1, 4.1, 9.1), xpd=TRUE)
#   , legend=colnames(has_similar), args.legend = list(x=56, bty = "n")
  barplot(t(has_read), beside=T, las=1)
#   barplot(t(has_context), beside=T, las=1)
#   barplot(t(has_gap), beside=T, las=1)
#   barplot(t(has_similar), beside=T, las=1)
  
}

profile_graph = function(){
  
  profile = read.csv("~/Projects/storyline/apps/graphs/profile_table.csv", header=F)
  names(profile) = c("gender", "age", "edu")
  par(mar = c(5.1, 4.1, 4.1, 6.1), xpd=TRUE)

#   gender_label = c("Nenhum/Outro", "Masculino", "Feminino")
#   gender = c( length(profile$gender[profile$gender == "Neither/Other"]),
#               length(profile$gender[profile$gender == "Male"]),
#               length(profile$gender[profile$gender == "Female"]))
#   
#   percent_label = round(gender / sum(gender) * 100, 1)
#   percent_label <- paste(gender_label, ' (', percent_label, ' %)', sep='')
#   
#   pdf("~/Projects/storyline/apps/graphs/gender.pdf", family="CMU Serif", width=6, height=4)
#   pie(gender, labels=percent_label, col = gray(seq(0.7, 1.0, length=3)))
#   dev.off()
  
#   edu_label = c("Nenhum/Outro", "Ensino M\u00E9dio", "Gradua\u00E7\u00E3o", "P\u00F3s-Gradua\u00E7\u00E3o")
#   edu = c(length(profile$edu[profile$edu == "Neither/Other"]),
#           length(profile$edu[profile$edu == "High School"]),
#           length(profile$edu[profile$edu == "Undergraduate"]),
#           length(profile$edu[profile$edu == "Graduate"])
#            )
#   
#   percent_label = round(edu / sum(edu) * 100, 1)
#   percent_label <- paste(edu_label, ' (', percent_label, ' %)', sep='')
#   
#   pdf("~/Projects/storyline/apps/graphs/edu.pdf", family="CMU Serif", width=6, height=4)
#   pie(edu, labels=percent_label, col = gray(seq(0.6, 1.0, length=4)))
#   dev.off()
  
  age_label = c("Nenhum/Outro", "19 a 23", "24 a 28", "29 a 33", "34 a 38", "39 a 43", "44 a 48")
  age = c(
    length(profile$age[profile$age == "Neither/Other"]),
    length(profile$age[profile$age == "19 to 23"]),
    length(profile$age[profile$age == "24 to 28"]),
    length(profile$age[profile$age == "29 to 33"]),
    length(profile$age[profile$age == "34 to 38"]),
    length(profile$age[profile$age == "39 to 43"]),
    length(profile$age[profile$age == "44 to 48"])
    )
  percent_label = round(age / sum(age) * 100, 1)
  percent_label <- paste(age_label, ' (', percent_label, ' %)', sep='')
  
  pdf("~/Projects/storyline/apps/graphs/age.pdf", family="CMU Serif", width=6, height=4)
  pie(age, labels=percent_label, col = gray(seq(0.4, 1.0, length=6)))
  dev.off()

}

userstory_amount_graph = function(){
  
  
  amount = read.csv("~/Projects/storyline/apps/graphs/userstory_amount_table.csv", header=F)
  names(amount) = c("Story", "Quantidade")
  rownames(amount) = amount$Story
  
  pdf("~/Projects/storyline/apps/graphs/userstory_amount.pdf", family="CMU Serif", width=5, height=4)
  barplot(t(amount[-1]), beside=F, las=1, ylim=c(0,100), xlab="Encadeamento (ID)", ylab="Usu\u00E1rio (%)")
  dev.off()
}

density_graph = function(story, ymax, m, meth, namexlab){
  
  data = read.csv(paste("~/Projects/storyline/apps/graphs/csv/storyline_",meth,"_table.csv", sep=""), header=F)
  data = t(data)
  colnames(data) = data[1,]
  data = data[-1,]
  rownames(data) = seq(from=1, to=length(data[,1]))
  
  data_rb = read.csv(paste("~/Projects/storyline/apps/graphs/csv/relevance_bm25f_",meth,"_table.csv", sep=""), header=F)
  data_rb = t(data_rb)
  colnames(data_rb) = data_rb[1,]
  data_rb = data_rb[-1,]
  rownames(data_rb) = seq(from=1, to=length(data_rb[,1]))
  
  data_rt = read.csv(paste("~/Projects/storyline/apps/graphs/csv/relevance_tfidf_",meth,"_table.csv", sep=""), header=F)
  data_rt = t(data_rt)
  colnames(data_rt) = data_rt[1,]
  data_rt = data_rt[-1,]
  rownames(data_rt) = seq(from=1, to=length(data_rt[,1]))
  
  data_tb = read.csv(paste("~/Projects/storyline/apps/graphs/csv/timeline_bm25f_",meth,"_table.csv", sep=""), header=F)
  data_tb = t(data_tb)
  colnames(data_tb) = data_tb[1,]
  data_tb = data_tb[-1,]
  rownames(data_tb) = seq(from=1, to=length(data_tb[,1]))
  
  data_tt = read.csv(paste("~/Projects/storyline/apps/graphs/csv/timeline_tfidf_",meth,"_table.csv", sep=""), header=F)
  data_tt = t(data_tt)
  colnames(data_tt) = data_tt[1,]
  data_tt = data_tt[-1,]
  rownames(data_tt) = seq(from=1, to=length(data_tt[,1]))
  
  pdf(paste("~/Projects/storyline/apps/graphs/pdf/d", m, story, ".pdf", sep=""), family="CMU Serif", width=5, height=4)
  plot(density(data[,story], na.rm = T, from=-2, to=2), type='l', lwd=1, lty='solid', xlab=namexlab, ylab='', main='', ylim=c(0,ymax), las=1)
  lines(density(data_rb[,story], na.rm = T, from=-2, to=2), type='l', lwd=1, lty="dashed")
#   lines(density(data_rt[,story], na.rm = T, from=-2, to=2), type='l', lwd=1, lty="dotdash")
#   lines(density(data_tb[,story], na.rm = T, from=-2, to=2), type='l', lwd=1, lty="longdash")
  lines(density(data_tt[,story], na.rm = T, from=-2, to=2), type='l', lwd=1, lty="dotted")
#  legend("topleft", c("Mecanismo", "Tempo TF-IDF","Relev\u00E2ncia BM25F"), lty=c('solid', 'dotted', 'dashed'), lwd=c(2,2,2), bty='n')
  dev.off()
}

create_densities = function(ma, metha, namexlaba) {
  
  density_graph(story=1, ymax=2.5, m=ma, meth=metha, namexlab=namexlaba)
  
  density_graph(story=2, ymax=3, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=3, ymax=0.8, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=4, ymax=0.8, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=5, ymax=3.5, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=6, ymax=3.5, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=7, ymax=4, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=8, ymax=2.5, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=9, ymax=3.5, m=ma, meth=metha, namexlab=namexlaba)
  density_graph(story=10, ymax=1.5, m=ma, meth=metha, namexlab=namexlaba)
  
}