package com.lube.webinspector.CrawlerTest;

import org.json.JSONException;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.lube.webinspector.Crawler.*;

import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

@SpringBootTest
class CrawlerToTest {

    @Test
    void crawlerTest() throws Exception {

        CrawlConfig config = new CrawlConfig();

        // Set the folder where intermediate crawl data is stored (e.g. list of urls
        // that are extracted from previously
        // fetched pages and need to be crawled later).
        config.setCrawlStorageFolder("src/main/resources/static/crawler4j/");

        // Number of threads to use during crawling. Increasing this typically makes
        // crawling faster. But crawling
        // speed depends on many other factors as well. You can experiment with this to
        // figure out what number of
        // threads works best for you.
        int numberOfCrawlers = 8;

        // Where should the downloaded images be stored?
        File storageFolder = new File("src/main/resources/static/images/");

        // Since images are binary content, we need to set this parameter to
        // true to make sure they are included in the crawl.
        config.setIncludeBinaryContentInCrawling(true);

        List<String> crawlDomains = Arrays.asList("https://www.lubecreostorepratolapeligna.it/");

        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        robotstxtConfig.setEnabled(false);
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        // qui aggiunge al controller tutti i seed
        for (String domain : crawlDomains) {
            controller.addSeed(domain);
        }

        if (!storageFolder.exists()) {
            storageFolder.mkdirs();
        }

        CrawlController.WebCrawlerFactory<Crawler> factory = () -> new Crawler(storageFolder, crawlDomains);
        controller.start(factory, numberOfCrawlers);

    }

    @Test
    void testImage() throws JSONException {
        File image1 = new File("src/main/resources/static/matching/image1.png");
        File image2 = new File("src/main/resources/static/matching/image2.png");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        //headers.setAccept(Collections.singletonList(MediaType.MULTIPART_FORM_DATA));
        headers.set("Api-Key", "quickstart-QUdJIGlzIGNvbWluZy4uLi4K");
        String url = "https://api.deepai.org/api/image-similarity";
        // request body parameters
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("image1", new FileSystemResource(image1));
        body.add("image2", new FileSystemResource(image2));

        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);
       
        ResponseEntity<String> response = new RestTemplate().postForEntity(url, entity, String.class);
        // get JSON response
         String json = response.getBody();
        JSONObject jsonObject = new JSONObject(json.toString());
        System.out.println(json);
    }

}
