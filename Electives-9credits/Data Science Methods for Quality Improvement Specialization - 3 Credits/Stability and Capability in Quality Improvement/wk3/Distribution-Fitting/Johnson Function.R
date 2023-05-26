djohn<-function(x,
                gamma,
                delta,
                xi,
                lambda
                #,type
){
  if (length(x) == 0) {
    numeric(0)
  } else {
    if (any(is.na(x))) {
      rep(NA, length(x))
    } else if (any(is.infinite(x)) | any(is.nan(x))) {
      rep(NaN, length(x))
    }else {
      dJohnson(x, list(gamma,delta,xi,lambda,type="SU")) 
    }
  }
}
pjohn<-function(q
                ,gamma
                ,delta
                ,xi
                ,lambda
                #,type
) {
  if (length(q) == 0) {
    numeric(0)
  } else {
    if (any(is.na(q))) {
      rep(NA, length(q))
    } else if (any(is.infinite(q)) | any(is.nan(q))) {
      rep(NaN, length(q))
    }else {
      pJohnson(q, list(gamma,delta,xi,lambda,type="SU")) 
    }
  }
}
qjohn<-function(p,gamma,delta,xi,lambda,type="SU") {
  if (length(p) == 0) {
    numeric(0)
  } else {
    if (any(is.na(p))) {
      rep(NA, length(p))
    } else if (any(is.infinite(p)) | any(is.nan(p))) {
      rep(NaN, length(p))
    }else {
      
      qJohnson(p, list(gamma,delta,xi,lambda,type))
    }
  }
}