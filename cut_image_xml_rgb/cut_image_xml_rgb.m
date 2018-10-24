clc;
clear;
path='F:\DATASETS\Car_Detection\VOC_cardetection\train\cashi\Annotations\';%源xml
path2='F:\DATASETS\Car_Detection\VOC_cardetection\train\cashi\JPEGImages_final\';%源jpg
path3='F:\DATASETS\Car_Detection\VOC_cardetection\train\cashi\image_crop1\';%裁切结果
dirs=dir(path);
flag=0;
flag1=0;
part=[];

count=0;
for i=3:length(dirs)
    count=count+1;
    disp(count);
    
    namenum=1;
    xml_name=dirs(i).name;
    name=xml_name(1:end-4);   
    img_name=[name,'.jpg'];
    img=imread([path2,img_name]);
    xml_read=[path,xml_name];
%     des2=[root3,xml_name]; 
    xDoc=xmlread(xml_read);
%     xRoot=xDoc.getDocumentElement();
    ob= xDoc.getElementsByTagName('object');
    for j=1:ob.getLength 
        k=1;
        thisItem = ob.item(j-1);
        childNode = thisItem.getFirstChild ;
        while ~isempty(childNode)
            if  childNode.getNodeType ~= 3 ;
                childNodeNm = char(childNode.getTagName); 
                childNodedata = char(childNode.getFirstChild.getData); 
                switch(childNodeNm)
                    case 'name'
                     Obj.name=childNodedata;
                    case 'pose'
                     Obj.pose=childNodedata;
                     case 'truncated'
                     Obj.truncated=childNodedata;
                     case 'difficult'
                     Obj.difficult=childNodedata;
                     case 'part'
                         temp=childNode.getElementsByTagName('name');
                         part(k).name=temp.item(0).item(0).getData;
                         
                         temp1=childNode.getElementsByTagName('xmin');
                         part(k).xmin=temp1.item(0).item(0).getData;
                         temp2=childNode.getElementsByTagName('ymin');
                         part(k).ymin=temp2.item(0).item(0).getData;
                         temp3=childNode.getElementsByTagName('xmax');
                         part(k).xmax=temp3.item(0).item(0).getData;
                         temp4=childNode.getElementsByTagName('ymax');
                         part(k).ymax=temp4.item(0).item(0).getData;
                         k=k+1;
                     case 'bndbox'
                         temp1=childNode.getElementsByTagName('xmin');
                         Obj.xmin=temp1.item(0).item(0).getData;
                         temp2=childNode.getElementsByTagName('ymin');
                         Obj.ymin=temp2.item(0).item(0).getData;
                         temp3=childNode.getElementsByTagName('xmax');
                         Obj.xmax=temp3.item(0).item(0).getData;
                         temp4=childNode.getElementsByTagName('ymax');
                         Obj.ymax=temp4.item(0).item(0).getData;
                    otherwise
                end
              end
            childNode = childNode.getNextSibling;
         end
            
              name_dir= [path3 Obj.name];
              if ~exist( name_dir,'dir')
              mkdir(name_dir);
              end
%               if exist([name_dir,'\',img_name],'file')
%               img1=imread([name_dir,'\',img_name]);
%               else
%                img1=img;
%               end
                   x1=str2num(Obj.ymin);
                   x2=str2num(Obj.ymax);
                   y1=str2num(Obj.xmin);
                   y2=str2num(Obj.xmax);

                     img1=img(x1:x2,y1:y2,:);
                    % img1=imresize(img1,[300,300]);

              
%             img2_name=[path3,name_dir,'\',name,'_',num2str(namenum),'_',num2str(Obj.truncated),'_',num2str(Obj.difficult)','.jpg'];
              %img2_name=[name_dir,'\',name,'_',num2str(namenum),'.jpg'];
              img2_name=[name_dir,'\',name,'.jpg'];
              imwrite(img1,img2_name);
              namenum=namenum+1;
              
% %               pt=[str2num(Obj.xmin),str2num(Obj.ymin)];
% %               wSize=[str2num(Obj.xmax)-str2num(Obj.xmin),str2num(Obj.yma   x)-str2num(Obj.ymin)];
% %               if (~isempty(wSize))&&wSize(1)>1&&wSize(2)>1
% %                  try
% %                 % img1= drawRect(img1,pt,wSize,5 );
% %                 
% %                  catch
% %                      img_name
% %                      Obj.name 
% %                  end
%                  %textColor    = [255, 255, 255];
%                 % textLocation = [str2num(Obj.xmin) str2num(Obj.ymin);str2num(Obj.xmin) str2num(Obj.ymin)+12;str2num(Obj.xmin) str2num(Obj.ymin)+22];
% %                  text_content=[Obj.name,' ',Obj.pose,'',Obj.truncated,Obj.difficult];
%                 % trunc_diffic=[Obj.truncated,' ',Obj.difficult];
%                  %strings = uint8([Obj.name 0 Obj.pose 0 trunc_diffic]);
%                  %textInserter = vision.TextInserter('%s','LocationSource','Input port','Color', textColor ,'FontSize',11);
% %                  textInserter = vision.TextInserter(text_content,'Color', textColor, 'FontSize', 11, 'Location', textLocation);
% %                  img1 = step(textInserter, img1);
%                 % img1 = step(textInserter, img1, strings, int32(textLocation));
% %                  imshow(img1)
% %               else
% %                   Obj.name
% %                   Obj.xmin
% %                   Obj.ymin
% %                   Obj.xmax
% %                   Obj.ymax
% %               end
%              if ~isempty(part)
%              for num=1:length(part)/4
%                   pt=[round(str2num(part(num).xmin)),round(str2num(part(num).ymin))];
%                  wSize=[round(str2num(part(num).xmax))-round(str2num(part(num).xmin)),round(str2num(part(num).ymax))-round(str2num(part(num).ymin))];
%                  if (~isempty(wSize))&&wSize(1)>1&&wSize(2)>1
%                      try
%                      img1= drawRect(img1,pt,wSize,5 );
%                      catch
%                      img_name
%                      part(num).name
%                      end
% %                      textColor    = [255, 0, 255];
% %                      textLocation = [round(str2num(part(num).xmin)) round(str2num(part(num).ymin))];
% %                      text_content=part(num).name;
% %                      text_content=char(text_content);
% %                      textInserter = vision.TextInserter(text_content,'Color', textColor, 'FontSize', 12, 'Location', textLocation);
% %                      img1= step(textInserter, img1);
%                   else
%                       part(num).name
%                       part(num).xmin
%                       part(num).ymin
%                       part(num).xmax
%                       part(num).ymax
%                   end
%              end
%              part=[];
%              end
%             imwrite(img1,[name_dir,'\',img_name]);

            
              
 end
%     fileName1=fileNames.item(0);
%     fileName1.setTextContent(img_name);%设置fileName1的文本内容
    
    
%     xmlwrite(des2,xDoc); 
end
disp('done!!');


% for i=3:length(dirs)
%     fold=fopen([path,dirs(i).name],'r');
%     name1=[dirs(i).name(1:end-4),'.jpg'];
%     img_path=[path2,name1];
%     %name2=[path2,dirs(i).name];
%     %fnew=fopen(name2,'w');
%     img=imread(img_path);
%     %line=1;
%     while ~feof(fold)
%         tline=fgetl(fold);
%         %if line==3
%        loc=strfind(tline, '<object>');
%        if loc
%        flag=1;
%        end
%        
%        if flag
%           flag1=flag1+1;
%           if flag1==2
%               l1=strfind(tline, '<name>');
%               l2=strfind(tline, '</name>');
%               name_dir=tline(l1+6:l2-1);
%               if ~exist(name_dir,'dir')
%               mkdir(name_dir);
%               end
%               if exist([name_dir,'\',name1],'file')
%               img1=imread([name_dir,'\',name1]);
%               else
%                img1=img;
%               end
%               
%           end
%           if flag1==7
%               l1=strfind(tline, '<xmin>');
%               l2=strfind(tline, '</xmin>');
%               xmin=tline(l1+6:l2-1);
%               xmin=str2num(xmin);
%           end
%           if flag1==8
%               l1=strfind(tline, '<ymin>');
%               l2=strfind(tline, '</ymin>');
%               ymin=tline(l1+6:l2-1);
%               ymin=str2num(ymin);
%           end
%           if flag1==9
%               l1=strfind(tline, '<xmax>');
%               l2=strfind(tline, '</xmax>');
%               xmax=tline(l1+6:l2-1);
%               xmax=str2num(xmax);
%           end
%           if flag1==10
%               l1=strfind(tline, '<ymax>');
%               l2=strfind(tline, '</ymax>');
%               ymax=tline(l1+6:l2-1);
%               ymax=str2num(ymax);
%               pt=[xmin,ymin];
%               wSize=[xmax-xmin,ymax-ymin];
%               if (~isempty(wSize))&&wSize(1)>3&&wSize(2)>3
%                  des = drawRect(img1,pt,wSize,5 );
%               else
%                  disp(name1); 
%                  tline
%                  xmin
%                  ymin
%                  xmax
%                  ymax
%               end
%               imwrite(des,[name_dir,'\',name1]);
%               flag=0;
%               flag1=0;
%               name_dir='';
%           end
%           
%        end
%        
%     end
% 
%     fclose(fold);
%  
% end