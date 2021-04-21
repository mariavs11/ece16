

bool detectTaps(){
  if ( (ax > 2080 && az > 2420) or (ax > 2080 && az < 2420) or (ax < 1945 && az > 2530) or (ax < 1945 && az < 2420) 
  
or (ay > 2015 && ax > 2080 ) or (ay > 2015 && ax < 1930) or (ay < 1930 && ax > 2080) or (ay < 1930 && ax < 1930)  
 or (ay > 2015 && az > 2520 ) or (ay > 2015 && az < 2420) or (ay < 1920 && az > 2530) or (ay < 1930 && az < 2420)
  // changed ax from 1950 to 1940
  // az 2420 to 2375
){
    return true;
    
    }
  else {
    return false;
    }
  }
