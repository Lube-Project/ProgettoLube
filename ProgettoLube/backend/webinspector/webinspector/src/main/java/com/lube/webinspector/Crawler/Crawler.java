package com.lube.webinspector.Crawler;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.collect.ImmutableList;
import com.google.common.io.Files;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.BinaryParseData;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

/**
 * This class shows how you can crawl images on the web and store them in a
 * folder. This is just for demonstration purposes and doesn't scale for large
 * number of images. For crawling millions of images you would need to store
 * downloaded images in a hierarchy of folders
 */
public class Crawler extends WebCrawler {

    private static final Pattern filters = Pattern.compile(
            ".*(\\.(css|js|mid|mp2|mp3|mp4|wav|avi|mov|mpeg|ram|m4v|pdf" + "|rm|smil|wmv|swf|wma|zip|rar|gz))$");

    private static final Pattern imgPatterns = Pattern.compile(".*(\\.(bmp|gif|jpe?g|png|tiff?))$");

    private File storageFolder;
    private List<String> crawlDomains;

    public Crawler(File storageFolder, List<String> crawlDomains) {
        this.storageFolder = storageFolder;
        this.crawlDomains = ImmutableList.copyOf(crawlDomains);
    }

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String href = url.getURL().toLowerCase();
        
        // TODO: HO COMMENTATO COSI VISITA SOLO IL SEED
        // filtro
        if (filters.matcher(href).matches()) {
            System.out.println("No Visit "+url.getURL());
            return false;
        }

        // per le immagini
        if (imgPatterns.matcher(href).matches()) {
            System.out.println("To Visit "+url.getURL());
            return true;
        }
        // sotto domini

        /*for (String domain : crawlDomains) {
            if (href.startsWith(domain)) {
                return true;
            }
        }*/

        return false;
    }

    @Override
    public void visit(Page page) {
        String url = page.getWebURL().getURL();
        String keysearch = "Lube";
        // TO SEARCH ON SITE
        System.out.println("URL: " + url);

        if (page.getParseData() instanceof HtmlParseData) {
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            String text = htmlParseData.getText(); // extract text from page
            String html = htmlParseData.getHtml(); // extract html from page
            Document doc = Jsoup.parseBodyFragment(html);
            // jsoup to search img tag
            Elements img = doc.getElementsByTag("img");
            ArrayList<String> urlTagImg = new ArrayList<String>();
            for (Element el : img) {
                urlTagImg.add("https://www.lubecreostorepratolapeligna.it/"+el.attr("src"));
            }
            //urlTagImg.forEach(string->{System.out.println(string);});
            System.out.println("size : "+urlTagImg.size());
            Set<WebURL> links = htmlParseData.getOutgoingUrls();

            System.out.println("---------------------------------------------------------");
            System.out.println("Page URL: " + url);
            System.out.println("Text length: " + text.length());
            System.out.println("Html length: " + html.length());
            System.out.println("Number of outgoing links: " + links.size());
            System.out.println("---------------------------------------------------------");

            /** CERCA TAG IMG */
            /*
             * Pattern pattern = Pattern.compile(
             * "(<img\\b|(?!^)\\G)[^>]*?\\b(src|width|height)=([\"']?)([^\"]*)\\3"); Matcher
             * matcher = pattern.matcher(html); while (matcher.find()) { if
             * (!matcher.group(1).isEmpty()) { // We have a new IMG tag
             * System.out.println("\n--- NEW MATCH ---"); }
             * System.out.println(matcher.group(2) + ": " + matcher.group(4)); }
             */
            if (text.contains(keysearch) || html.contains(keysearch)) {
                System.out.println("KEYWORD MATCHED");
            } else {
                System.out.println("KEYWORD NOT MATCHED");
            }
        }
        // TO STORE IMAGES

        // We are only interested in processing images which are bigger than 10k
        if (!imgPatterns.matcher(url).matches() || !((page.getParseData() instanceof BinaryParseData)
                || (page.getContentData().length < (10 * 1024)))) {
            return;
        }

        // Get a unique name for storing this image
        String extension = url.substring(url.lastIndexOf('.'));
        String hashedName = UUID.randomUUID() + extension;

        // Store image
        String filename = storageFolder.getAbsolutePath() + '/' + hashedName;
        try {
            Files.write(page.getContentData(), new File(filename));
            WebCrawler.logger.info("Stored: {}", url);
        } catch (IOException iox) {
            WebCrawler.logger.error("Failed to write file: {}", filename, iox);
        }
    }

}
