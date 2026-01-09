# Short Data Set Exfiltration

Basic demonstration example of risks - how to bypass I/O file scanning to exfiltrate short data sets in a scenario where images are allow-listed but text and file content is scanned and where most file-types are blocked by network filters. 

Use case is to be able to send an image that can be embedded into another image with short exfiltrated data in a way that is not detectable without intensive manual investigation.
  
 Currently relies on factor, xxd, ImageMagick, to be truly usable those would be replaced by home-rolled utilities in order to only leverage what is on a Unix/Linux system by default.
 
 Many improvements still needed. Not used in live systems, exists purely as a proof of concepts.
 
 
