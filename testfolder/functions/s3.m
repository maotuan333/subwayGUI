function [] = s3(file_name)
    fid=fopen([extractBefore(file_name,'3.zip') '4.txt'],'w');
    fclose(fid);
end