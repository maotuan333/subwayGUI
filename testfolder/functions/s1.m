function [] = s1(file_name)
    fid=fopen([extractBefore(file_name,'1.docx')  '2.pub'],'w');
    fclose(fid);
end