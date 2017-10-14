//  ref : https://github.com/MerHS/biryo 
import java.io.*;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class refine {
 
  public static void main(String args[])
  {
    int i = 1;
    for(i=1;i<2;i++)
    {
      try{
    
      BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream("Cnamu_00"+i+".txt"),"utf-8"));
      BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("namu_00"+i+".txt"),"utf-8"));
      String s,s_r;
     
      while((s = in.readLine()) != null){
        s_r = s.replaceAll("<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>", " ");
        StringTokenizer tk = new StringTokenizer(s_r," ");
        String token;
      
        while(tk.hasMoreTokens()){
          token = StringReplace(tk.nextToken());
          bw.write(token + " ");
        }
      bw.write("\n");
      
      }

      in.close();
      bw.close();

      System.out.println("aaaa");
      } catch(IOException e){
      System.err.println(e);
      System.exit(1);
     }
    }
  }
 
 
  public static String StringReplace(String str){

    String str_2;
      
      str_2 = str.replaceAll("([\\p{Alnum}]+)//([A-Za-z0-9.\\-&/%=?:@#$(),.+;~\\_]+)", " ");
      str_2 = str_2.replaceAll("([\\p{Alnum}]+)://([A-Za-z0-9.\\-&/%=?:@#$(),.+;~\\_]+)", " ");
      str_2 = str_2.replaceAll("[〈〉=#\\$%&\\(\\)\\{\\}\\@\\`\\*:\\+\\;\\-\\.<>,\\^~|'\\[\\]\\|\\\\\"《》/●→]", " ");
      str_2 = str_2.replaceAll("url|INDEX|close|ref", " ");
      str_2 = str_2.replaceAll("(open+[0-99]+[0-99])|(open+[0-99])"," ");
      str_2 = str_2.replaceAll("(h+[0-99]+[0-99])|(h+[0-99])"," ");


    return str_2;
  }
   
 /*
 private static String getText(String content) {
  Pattern SCRIPTS = Pattern.compile("<(no)?script[^>]*>.*?</(no)?script>",Pattern.DOTALL);
  Pattern STYLE = Pattern.compile("<style[^>]*>.*</style>",Pattern.DOTALL);
  Pattern TAGS = Pattern.compile("<(\"[^\"]*\"|\'[^\']*\'|[^\'\">])*>");
  Pattern nTAGS = Pattern.compile("<\\w+\\s+[^<]*\\s*>");
  Pattern ENTITY_REFS = Pattern.compile("&[^;]+;");
  Pattern WHITESPACE = Pattern.compile("\\s\\s+");
  
  Matcher m;
  
  m = SCRIPTS.matcher(content);
  content = m.replaceAll("");
  m = STYLE.matcher(content);
  content = m.replaceAll("");
  m = TAGS.matcher(content);
  content = m.replaceAll("");
  m = ENTITY_REFS.matcher(content);
  content = m.replaceAll("");
  m = WHITESPACE.matcher(content);
  content = m.replaceAll(" ");   
  
  return content;
 }
*/
}
