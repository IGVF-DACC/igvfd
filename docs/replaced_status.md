# Replaced Status
Accessioned objects have a special status of replaced that allows them to share identifying properties like md5sum or accession.  This essentially allows us to merge two objects. Here is a [link](https://docs.google.com/presentation/d/1uMDHw0MQBb3mMxOWm88cSq6aRWbn2KpZyHHI5yQMQAE/edit?pli=1&slide=id.g7171591498_0_295#slide=id.g7171591498_0_295) to ENCODE status slides in general.

## Why do we have a replaced status
Each schema has a list of identifying properties. These properties can be used in the url to access the object (see examples).  The values in these properties must be unique so that each value resolves to one and only one object.  However, there are many situations where you would want to have more than one object "merge" or all be directed to the same object.  To achieve that, we use the replaced status to release all identifying properties except the uuid.  We use the alternate_accessions property to redirect to the correct object. 

Examples:
* **accession:** [https://data.igvf.org/sequence-files/IGVFFI0196UOBL/](https://data.igvf.org/sequence-files/IGVFFI0196UOBL/)
* **uuid:** [https://data.igvf.org/sequence-files/929fa984-ad15-4f1b-ab07-df05e0f18856/](https://data.igvf.org/sequence-files/929fa984-ad15-4f1b-ab07-df05e0f18856/)

## Reasons to use *replaced* status

* **MD5SUM CONFLICT** Objects are never deleted, they are set to status = deleted.  Md5sums are set as *identifying properties* therefore two objects of the same md5sum create a concflict.  If, for whatever reason, a file object needs to be replaced but the file is the same or if the same file needs to be submitted twice.  The replaced status allows the two files to share the same md5sum.
* **TYPE CHANGE** If an object was accidentally submitted as the wrong type (i.e. primary cell instead of tissue) you will have to create a new object.  If you want the existing accession to be reused on the new object, you can set the old object as replaced and the two objects can share an accession.
* **CLASSIC MERGE**  If two labs submit an object like a donor that turn out to be the same donor, you can use replaced to merge the two objects.  Example:  Lab A submits a donor object for K562 and Lab B also submits a donor object for K562.  We want one object but we want to keep all of the identifiers.

## Steps to use the *replaced* status

1. Note the accession(s) and uuid(s) of the object(s) you are about to replace.  
2. Set "old" object(s) to replaced
3. Import or Update the new object(s) with “alternate_accession”:[“OLDOBJECTACCESSION”]

ENCODE example:
* [https://www.encodeproject.org/files/7cabddfa-a1cd-4880-b1cf-a9a0650bc592/](https://www.encodeproject.org/files/7cabddfa-a1cd-4880-b1cf-a9a0650bc592/)
* [https://www.encodeproject.org/files/ENCFF052HRS/](https://www.encodeproject.org/files/ENCFF052HRS/)
* [https://www.encodeproject.org/files/ENCFF987JHY/](https://www.encodeproject.org/files/ENCFF987JHY/)

