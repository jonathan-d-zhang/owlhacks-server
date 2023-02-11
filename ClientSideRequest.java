import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.IOException;
import java.net.Authenticator;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpResponse;
import java.util.Scanner;
import java.net.http.HttpRequest;

public class ClientSideRequest {
    public static void main(String[] args) throws IOException, InterruptedException {
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create("http://172.104.14.22/open"))
                    .POST(HttpRequest.BodyPublishers.noBody())
                    .build();
            var x = client.send(req, HttpResponse.BodyHandlers.ofString());
            System.out.println(x.body());

            //ID - what the last data from the server was
            //Words translated


            //Check if connect is made

                StringBuilder informationString = new StringBuilder();
                /*Scanner scanner = new Scanner(.getInputStream());

                /*while (scanner.hasNext()) {
                    informationString.append(scanner.nextLine());
                }
                //Close the scanner
                scanner.close();

                System.out.println(informationString);


                //JSON simple library Setup with Maven is used to convert strings to JSON
                JSONParser parse = new JSONParser();
                JSONArray dataObject = (JSONArray) parse.parse(String.valueOf(informationString));

                //Get the first JSON object in the JSON array
                System.out.println(dataObject.get(0));

                JSONObject countryData = (JSONObject) dataObject.get(0);

                System.out.println(countryData.get("location_id"));

            }
        } catch (Exception e) {
            e.printStackTrace();
        }

             */
    }

}