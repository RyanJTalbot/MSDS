### Lab: Deep Learning

## In this version of the Ch10 lab, we  use the `luz` package, which interfaces to the
## `torch` package which in turn links to efficient
## `C++` code in the LibTorch library.

## This version of the lab was produced by Daniel Falbel and Sigrid
## Keydana, both data scientists at Rstudio where these packages were
## produced.

## An advantage over our original `keras` implementation is that this
## version does not require a separate `python` installation.

## Single Layer Network on Hitters Data


###
library(ISLR2)
Gitters <- na.omit(Hitters)
n <- nrow(Gitters)
set.seed(13)
ntest <- trunc(n / 3)
testid <- sample(1:n, ntest)
###

###
lfit <- lm(Salary ~ ., data = Gitters[-testid, ])
lpred <- predict(lfit, Gitters[testid, ])
with(Gitters[testid, ], mean(abs(lpred - Salary)))
###


###
x <- scale(model.matrix(Salary ~ . - 1, data = Gitters))
y <- Gitters$Salary
###


###
library(glmnet)
cvfit <- cv.glmnet(x[-testid, ], y[-testid],
    type.measure = "mae")
cpred <- predict(cvfit, x[testid, ], s = "lambda.min")
mean(abs(y[testid] - cpred))
###

###
library(torch)
library(luz) # high-level interface for torch
library(torchvision) # for datasets and image transformation
library(torchdatasets) # for datasets we are going to use
library(zeallot)
torch_manual_seed(13)
###

###
modnn <- nn_module(
  initialize = function(input_size) {
    self$hidden <- nn_linear(input_size, 50)
    self$activation <- nn_relu()
    self$dropout <- nn_dropout(0.4)
    self$output <- nn_linear(50, 1)
  },
  forward = function(x) {
    x %>%
      self$hidden() %>%
      self$activation() %>%
      self$dropout() %>%
      self$output()
  }
)
###

###
x <- scale(model.matrix(Salary ~ . - 1, data = Gitters))
###


###
x <- model.matrix(Salary ~ . - 1, data = Gitters) %>% scale()
###

###
modnn <- modnn %>%
  setup(
    loss = nn_mse_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_mae())
  ) %>%
  set_hparams(input_size = ncol(x))
###

###
fitted <- modnn %>%
  fit(
    data = list(x[-testid, ], matrix(y[-testid], ncol = 1)),
    valid_data = list(x[testid, ], matrix(y[testid], ncol = 1)),
    epochs = 20
  )
###

###
plot(fitted)
###


###
npred <- predict(fitted, x[testid, ])
mean(abs(y[testid] - npred))
###

## Multilayer Network on the MNIST Digit Data


###
train_ds <- mnist_dataset(root = ".", train = TRUE, download = TRUE)
test_ds <- mnist_dataset(root = ".", train = FALSE, download = TRUE)

str(train_ds[1])
str(test_ds[2])

length(train_ds)
length(test_ds)
###


###
transform <- function(x) {
  x %>%
    torch_tensor() %>%
    torch_flatten() %>%
    torch_div(255)
}
train_ds <- mnist_dataset(
  root = ".",
  train = TRUE,
  download = TRUE,
  transform = transform
)
test_ds <- mnist_dataset(
  root = ".",
  train = FALSE,
  download = TRUE,
  transform = transform
)
###


###
modelnn <- nn_module(
  initialize = function() {
    self$linear1 <- nn_linear(in_features = 28*28, out_features = 256)
    self$linear2 <- nn_linear(in_features = 256, out_features = 128)
    self$linear3 <- nn_linear(in_features = 128, out_features = 10)

    self$drop1 <- nn_dropout(p = 0.4)
    self$drop2 <- nn_dropout(p = 0.3)

    self$activation <- nn_relu()
  },
  forward = function(x) {
    x %>%

      self$linear1() %>%
      self$activation() %>%
      self$drop1() %>%

      self$linear2() %>%
      self$activation() %>%
      self$drop2() %>%

      self$linear3()
  }
)
###


###
print(modelnn())
###


###
modelnn <- modelnn %>%
  setup(
    loss = nn_cross_entropy_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_accuracy())
  )
###

###
system.time(
   fitted <- modelnn %>%
      fit(
        data = train_ds,
        epochs = 5,
        valid_data = 0.2,
        dataloader_options = list(batch_size = 256),
        verbose = FALSE
      )
 )
plot(fitted)
###

###
accuracy <- function(pred, truth) {
   mean(pred == truth) }

# gets the true classes from all observations in test_ds.
truth <- sapply(seq_along(test_ds), function(x) test_ds[x][[2]])

fitted %>%
  predict(test_ds) %>%
  torch_argmax(dim = 2) %>%  # the predicted class is the one with higher 'logit'.
  as_array() %>% # we convert to an R object
  accuracy(truth)
###

###
modellr <- nn_module(
  initialize = function() {
    self$linear <- nn_linear(784, 10)
  },
  forward = function(x) {
    self$linear(x)
  }
)
print(modellr())
###

###
fit_modellr <- modellr %>%
  setup(
    loss = nn_cross_entropy_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_accuracy())
  ) %>%
  fit(
    data = train_ds,
    epochs = 5,
    valid_data = 0.2,
    dataloader_options = list(batch_size = 128)
  )

fit_modellr %>%
  predict(test_ds) %>%
  torch_argmax(dim = 2) %>%  # the predicted class is the one with higher 'logit'.
  as_array() %>% # we convert to an R object
  accuracy(truth)


# alternatively one can use the `evaluate` function to get the results
# on the test_ds
evaluate(fit_modellr, test_ds)
###

### Convolutional Neural Networks

###
transform <- function(x) {
  transform_to_tensor(x)
}

train_ds <- cifar100_dataset(
  root = "./",
  train = TRUE,
  download = TRUE,
  transform = transform
)

test_ds <- cifar100_dataset(
  root = "./",
  train = FALSE,
  transform = transform
)

str(train_ds[1])
length(train_ds)
###


###
par(mar = c(0, 0, 0, 0), mfrow = c(5, 5))
index <- sample(seq(50000), 25)
for (i in index) plot(as.raster(as.array(train_ds[i][[1]]$permute(c(2,3,1)))))
###

###
conv_block <- nn_module(
  initialize = function(in_channels, out_channels) {
    self$conv <- nn_conv2d(
      in_channels = in_channels,
      out_channels = out_channels,
      kernel_size = c(3,3),
      padding = "same"
    )
    self$relu <- nn_relu()
    self$pool <- nn_max_pool2d(kernel_size = c(2,2))
  },
  forward = function(x) {
    x %>%
      self$conv() %>%
      self$relu() %>%
      self$pool()
  }
)

model <- nn_module(
  initialize = function() {
    self$conv <- nn_sequential(
      conv_block(3, 32),
      conv_block(32, 64),
      conv_block(64, 128),
      conv_block(128, 256)
    )
    self$output <- nn_sequential(
      nn_dropout(0.5),
      nn_linear(2*2*256, 512),
      nn_relu(),
      nn_linear(512, 100)
    )
  },
  forward = function(x) {
    x %>%
      self$conv() %>%
      torch_flatten(start_dim = 2) %>%
      self$output()
  }
)
model()
###

###
fitted <- model %>%
  setup(
    loss = nn_cross_entropy_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_accuracy())
  ) %>%
  set_opt_hparams(lr = 0.001) %>%
  fit(
    train_ds,
    epochs = 10, #30,
    valid_data = 0.2,
    dataloader_options = list(batch_size = 128)
  )

print(fitted)

evaluate(fitted, test_ds)
###

###
img_dir <- "book_images"
image_names <- list.files(img_dir)
num_images <- length(image_names)
x <- torch_empty(num_images, 3, 224, 224)
for (i in 1:num_images) {
   img_path <- file.path(img_dir, image_names[i])
   img <- img_path %>%
     base_loader() %>%
     transform_to_tensor() %>%
     transform_resize(c(224, 224)) %>%
     # normalize with imagenet mean and stds.
     transform_normalize(
       mean = c(0.485, 0.456, 0.406),
       std = c(0.229, 0.224, 0.225)
     )
   x[i,,, ] <- img
}
###

###
model <- torchvision::model_resnet18(pretrained = TRUE)
model$eval() # put the model in evaluation mode
###

###
preds <- model(x)

mapping <- jsonlite::read_json("https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json") %>%
  sapply(function(x) x[[2]])

top3 <- torch_topk(preds, dim = 2, k = 3)

top3_prob <- top3[[1]] %>%
  nnf_softmax(dim = 2) %>%
  torch_unbind() %>%
  lapply(as.numeric)

top3_class <- top3[[2]] %>%
  torch_unbind() %>%
  lapply(function(x) mapping[as.integer(x)])

result <- purrr::map2(top3_prob, top3_class, function(pr, cl) {
  names(pr) <- cl
  pr
})
names(result) <- image_names
print(result)
###

## IMDb Document Classification

###
max_features <- 10000
imdb_train <- imdb_dataset(
  root = ".",
  download = TRUE,
  num_words = max_features
)
imdb_test <- imdb_dataset(
  root = ".",
  download = TRUE,
  num_words = max_features
)
###


###
imdb_train[1]$x[1:12]
###

###
word_index <- imdb_train$vocabulary
decode_review <- function(text, word_index) {
   word <- names(word_index)
   idx <- unlist(word_index, use.names = FALSE)
   word <- c("<PAD>", "<START>", "<UNK>", word)
   words <- word[text]
   paste(words, collapse = " ")
}
decode_review(imdb_train[1]$x[1:12], word_index)
###

###
library(Matrix)
one_hot <- function(sequences, dimension) {
   seqlen <- sapply(sequences, length)
   n <- length(seqlen)
   rowind <- rep(1:n, seqlen)
   colind <- unlist(sequences)
   sparseMatrix(i = rowind, j = colind,
      dims = c(n, dimension))
}
###

###
# collect all values into a list
train <- seq_along(imdb_train) %>%
  lapply(function(i) imdb_train[i]) %>%
  purrr::transpose()
test <- seq_along(imdb_test) %>%
  lapply(function(i) imdb_test[i]) %>%
  purrr::transpose()

# num_words + padding + start + oov token = 10000 + 3
x_train_1h <- one_hot(train$x, 10000 + 3)
x_test_1h <- one_hot(test$x, 10000 + 3)
dim(x_train_1h)
nnzero(x_train_1h) / (25000 * (10000 + 3))
###


###
set.seed(3)
ival <- sample(seq(along = train$y), 2000)
itrain <- seq_along(train$y)[-ival]
###

###
library(glmnet)
y_train <- unlist(train$y)

fitlm <- glmnet(x_train_1h[itrain, ], unlist(y_train[itrain]),
    family = "binomial", standardize = FALSE)
classlmv <- predict(fitlm, x_train_1h[ival, ]) > 0
acclmv <- apply(classlmv, 2, accuracy,  unlist(y_train[ival]) > 0)
###

###
par(mar = c(4, 4, 4, 4), mfrow = c(1, 1))
plot(-log(fitlm$lambda), acclmv)
###

###
model <- nn_module(
  initialize = function(input_size = 10000 + 3) {
    self$dense1 <- nn_linear(input_size, 16)
    self$relu <- nn_relu()
    self$dense2 <- nn_linear(16, 16)
    self$output <- nn_linear(16, 1)
  },
  forward = function(x) {
    x %>%
      self$dense1() %>%
      self$relu() %>%
      self$dense2() %>%
      self$relu() %>%
      self$output() %>%
      torch_flatten(start_dim = 1)
  }
)
model <- model %>%
  setup(
    loss = nn_bce_with_logits_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_binary_accuracy_with_logits())
  ) %>%
  set_opt_hparams(lr = 0.001)

fitted <- model %>%
  fit(
    # we transform the training and validation data into torch tensors
    list(
      torch_tensor(as.matrix(x_train_1h[itrain,]), dtype = torch_float()),
      torch_tensor(unlist(train$y[itrain]))
    ),
    valid_data = list(
      torch_tensor(as.matrix(x_train_1h[ival, ]), dtype = torch_float()),
      torch_tensor(unlist(train$y[ival]))
    ),
    dataloader_options = list(batch_size = 512),
    epochs = 10
  )

plot(fitted)
###

###
fitted <- model %>%
  fit(
    list(
      torch_tensor(as.matrix(x_train_1h[itrain,]), dtype = torch_float()),
      torch_tensor(unlist(train$y[itrain]))
    ),
    valid_data = list(
      torch_tensor(as.matrix(x_test_1h), dtype = torch_float()),
      torch_tensor(unlist(test$y))
    ),
    dataloader_options = list(batch_size = 512),
    epochs = 10
  )
###

## Recurrent Neural Networks


### Sequential Models for Document Classification



###
wc <- sapply(seq_along(imdb_train), function(i) length(imdb_train[i]$x))
median(wc)
sum(wc <= 500) / length(wc)
###

###
maxlen <- 500
num_words <- 10000
imdb_train <- imdb_dataset(root = ".", split = "train", num_words = num_words,
                           maxlen = maxlen)
imdb_test <- imdb_dataset(root = ".", split = "test", num_words = num_words,
                           maxlen = maxlen)

vocab <- c(rep(NA, imdb_train$index_from - 1), imdb_train$get_vocabulary())
tail(names(vocab)[imdb_train[1]$x])
###

###
model <- nn_module(
  initialize = function() {
    self$embedding <- nn_embedding(10000 + 3, 32)
    self$lstm <- nn_lstm(input_size = 32, hidden_size = 32, batch_first = TRUE)
    self$dense <- nn_linear(32, 1)
  },
  forward = function(x) {
    c(output, c(hn, cn)) %<-% (x %>%
      self$embedding() %>%
      self$lstm())
    output[,-1,] %>%  # get the last output
      self$dense() %>%
      torch_flatten(start_dim = 1)
  }
)
###

###
model <- model %>%
  setup(
    loss = nn_bce_with_logits_loss(),
    optimizer = optim_rmsprop,
    metrics = list(luz_metric_binary_accuracy_with_logits())
  ) %>%
  set_opt_hparams(lr = 0.001)

fitted <- model %>% fit(
  imdb_train,
  epochs = 10,
  dataloader_options = list(batch_size = 128),
  valid_data = imdb_test
)
plot(fitted)
predy <- torch_sigmoid(predict(fitted, imdb_test)) > 0.5
evaluate(fitted, imdb_test, dataloader_options = list(batch_size = 512))
###

###  Time Series Prediction

###
library(ISLR2)
xdata <- data.matrix(
 NYSE[, c("DJ_return", "log_volume","log_volatility")]
 )
istrain <- NYSE[, "train"]
xdata <- scale(xdata)
###

###
lagm <- function(x, k = 1) {
   n <- nrow(x)
   pad <- matrix(NA, k, ncol(x))
   rbind(pad, x[1:(n - k), ])
}
###


###
arframe <- data.frame(log_volume = xdata[, "log_volume"],
   L1 = lagm(xdata, 1), L2 = lagm(xdata, 2),
   L3 = lagm(xdata, 3), L4 = lagm(xdata, 4),
   L5 = lagm(xdata, 5)
 )
###

###
arframe <- arframe[-(1:5), ]
istrain <- istrain[-(1:5)]
###

###
arfit <- lm(log_volume ~ ., data = arframe[istrain, ])
arpred <- predict(arfit, arframe[!istrain, ])
V0 <- var(arframe[!istrain, "log_volume"])
1 - mean((arpred - arframe[!istrain, "log_volume"])^2) / V0
###

###
arframed <-
    data.frame(day = NYSE[-(1:5), "day_of_week"], arframe)
arfitd <- lm(log_volume ~ ., data = arframed[istrain, ])
arpredd <- predict(arfitd, arframed[!istrain, ])
1 - mean((arpredd - arframe[!istrain, "log_volume"])^2) / V0
###

###
n <- nrow(arframe)
xrnn <- data.matrix(arframe[, -1])
xrnn <- array(xrnn, c(n, 3, 5))
xrnn <- xrnn[,, 5:1]
xrnn <- aperm(xrnn, c(1, 3, 2))
dim(xrnn)
###

###
model <- nn_module(
  initialize = function() {
    self$rnn <- nn_rnn(3, 12, batch_first = TRUE)
    self$dense <- nn_linear(12, 1)
    self$dropout <- nn_dropout(0.2)
  },
  forward = function(x) {
    c(output, ...) %<-% (x %>%
      self$rnn())
    output[,-1,] %>%
      self$dropout() %>%
      self$dense() %>%
      torch_flatten(start_dim = 1)
  }
)

model <- model %>%
  setup(
    optimizer = optim_rmsprop,
    loss = nn_mse_loss()
  ) %>%
  set_opt_hparams(lr = 0.001)

###

###
fitted <- model %>% fit(
    list(xrnn[istrain,, ], arframe[istrain, "log_volume"]),
    epochs = 75, #epochs = 200,
    dataloader_options = list(batch_size = 64),
    valid_data =
      list(xrnn[!istrain,, ], arframe[!istrain, "log_volume"])
  )
kpred <- as.numeric(predict(fitted, xrnn[!istrain,, ]))
1 - mean((kpred - arframe[!istrain, "log_volume"])^2) / V0
###

###
model <- nn_module(
  initialize = function() {
    self$dense <- nn_linear(15, 1)
  },
  forward = function(x) {
    x %>%
      torch_flatten(start_dim = 2) %>%
      self$dense()
  }
)
###

###
x <- model.matrix(log_volume ~ . - 1, data = arframed)
colnames(x)
###

###
arnnd <- nn_module(
  initialize = function() {
    self$dense <- nn_linear(15, 32)
    self$dropout <- nn_dropout(0.5)
    self$activation <- nn_relu()
    self$output <- nn_linear(32, 1)

  },
  forward = function(x) {
    x %>%
      torch_flatten(start_dim = 2) %>%
      self$dense() %>%
      self$activation() %>%
      self$dropout() %>%
      self$output() %>%
      torch_flatten(start_dim = 1)
  }
)
arnnd <- arnnd %>%
  setup(
    optimizer = optim_rmsprop,
    loss = nn_mse_loss()
  ) %>%
  set_opt_hparams(lr = 0.001)

fitted <- arnnd %>% fit(
    list(xrnn[istrain,, ], arframe[istrain, "log_volume"]),
    epochs = 30, #epochs = 200,
    dataloader_options = list(batch_size = 64),
    valid_data =
      list(xrnn[!istrain,, ], arframe[!istrain, "log_volume"])
  )
plot(fitted)
npred <- as.numeric(predict(fitted, xrnn[!istrain, ,]))
1 - mean((arframe[!istrain, "log_volume"] - npred)^2) / V0
###
