function [] = s0(file_name)
    fid=fopen([extractBefore(file_name,'0.txt') '1.docx'],'w');
    fclose(fid);
end