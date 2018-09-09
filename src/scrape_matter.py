import json
from lxml import html
import requests
from urllib.parse import unquote

with open('../category_article.json') as f:
    data_root = json.load(f)

meta = {
    # "expert_review": "",
    "stats": "",
    # "quick_summary_section": "",
    # "sections": {},
    # "tip_section": "",
    # "warning_section": "",
    # "thingsyoullneed_section": "",
    # "qa_section": "",
    # "video_section": "",
    # "related_section": "",
    # "cite_section": "",
    # "info_section": "",
}

expert_review = {
    "name": "",
    "designation": "",
}

stats = {
    "no_of_votes": -1,
    "helpfulness": "",
    "coauthor_count": -1,
    "updated": "",
    "views" : -1,
}

quick_summary_section = {
    "quick_summary": [],
}

section = {
    "title": "",
    "steps": {}
}

tip_section = {
    "tips" : [],

}

thingsyoullneed_section = {
    "things": []
}

warning_section = {
    "warnings": [],
}

qa_section = {
    "qas": []
}

qa = {
    "question" : "",
    "answer" : "",
    "answerer": "",
    "helpful": -1,
    "not_helpful": -1,

}

video_section = {
    "video_url" : ""
}

related_section = {
    "urls": []
}

cite_section = {
    "cite": []
}

info_section = {
    "info_content": [],
}

step = {
    "pic_url": "",
    "title": "",
    "desc": "",
    "points": [],
}

def index_subs(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1

#list to string
def lts(lis):
    return ' '.join(lis)


def recurse(data):
    if data["children"]:
        for i in data["children"]:
            recurse(i)

    print(data["name"])
    for kk in data["content"]:
        stripped = kk["url"]
        page = requests.get(stripped)
        tree = html.fromstring(page.content)


        ####################################################
        #Article Information like Languages Available and Categories
        i_info_section = info_section.copy()
        i_info_section["info_content"] = unquote(lts(tree.xpath('//div[@id="article_info"]//text()')))


        ####################################################
        #Citations and References in the article
        i_cite_section = cite_section.copy()
        i_cite_section["cite"] = tree.xpath('//div[@id="sourcesandcitations"]/div/ol/li/span/a/text()')


        ####################################################
        #Links to other wikihow articles related to this article
        i_related_section = related_section.copy()
        i_related_section["urls"] = tree.xpath('//div[@id="relatedwikihows"]//a[@class="related-image-link"]/@href')


        ####################################################
        #Video in the article
        i_video_section = video_section.copy()
        i_video_section["video_url"] = tree.xpath('//div[@id="sourcesandcitations"]/div/ol/li/span/a/text()')


        ####################################################
        #Questions and Answers (including unanswered) of the article
        i_qa_section = qa_section.copy()
        for qas in tree.xpath('//div[@class="qa_li_container"]'):
            i_qa = qa.copy()
            i_qa["question"] = lts(qas.xpath('.//div[@class="qa_q_txt question" or @class="qa_q_txt"]/text()'))
            i_qa["answer"] = lts(qas.xpath('.//div[@class="qa_answer answer"]/text()'))
            i_qa["answerer"] = list(map(str.strip, qas.xpath('.//div[@class="qa_answerer_info"]//text()')))
            i_qa["helpful"] = lts(qas.xpath('.//a[@class="wh_vote_up wh_vote_box"]/span/text()'))
            i_qa["not_helpful"] = lts(qas.xpath('.//a[@class="wh_vote_down wh_vote_box"]/span/text()'))
            i_qa_section["qas"].append(i_qa)


        ####################################################
        #Warnings in the article
        i_warning_section = warning_section.copy()
        for warning in tree.xpath('//div[@id="warnings"]//li'):
            i_warning_section["warnings"].append((lts(warning.xpath('./text()'))).strip())


        ####################################################
        #Tips in the article
        i_tip_section = tip_section.copy()
        for tips in tree.xpath('//div[@id="tips"]//li'):
            i_tip_section["tips"].append(lts(tips.xpath('.//text()')))


        ####################################################
        #Things you'll need in the article
        i_thingsyoullneed_section = thingsyoullneed_section.copy()
        for things in tree.xpath('//div[@id="thingsyoullneed"]//li'):
            i_thingsyoullneed_section["things"].append((lts(things.xpath('.//text()'))).strip())


        ####################################################
        #Quick Summary Section from the article
        i_quick_summary_section = quick_summary_section.copy()
        i_quick_summary_section["quick_summary"] = lts(tree.xpath('//div[@id="quicksummary"]/p//text()'))


        ####################################################
        #Stats from the article
        i_stats = stats.copy()
        helpfulness = lts(tree.xpath('//div[@id="sp_helpful_rating_count"]/text()')).split(' votes - ')
        try:
            i_stats["no_of_votes"] = helpfulness[0]
            i_stats["helpfulness"] = helpfulness[1]
        except:
            pass
        i_stats["coauthor_count"] = lts(tree.xpath('//div[@id="sp_stats_box"]//*[contains(text(), "Co-authors")]/span/text()'))
        i_stats["updated"] = lts(tree.xpath('//div[@id="sp_stats_box"]//span[@id="sp_modified"]/@data-datestamp'))
        i_stats["views"] = lts(tree.xpath('//div[@id="sp_stats_box"]//*[contains(text(), "Views")]/span/text()'))


        ####################################################
        #To check whether the article is expert reviewed
        i_expert_review = expert_review.copy()
        i_expert_review["name"] = lts(tree.xpath('//div[@id="sp_expert_name"]//text()'))
        i_expert_review["designation"] = lts(tree.xpath('//div[@id="sp_expert_blurb"]//text()'))


        ####################################################
        #Sections of the article
        sections_dict = {}
        for sections in tree.xpath('//div[contains(@class, "section steps")]'):
            i_section = section.copy()
            i_section["title"] = lts(sections.xpath('.//h3/span/text()'))
            steps_dict = {}
            for steps in sections.xpath('.//ol[contains(@class, "steps_list_")]/li'):
                i_step = step.copy()
                i_step["pic_url"] = lts(steps.xpath('.//img/@src'))
                i_step["title"] = lts(steps.xpath('.//b[@class="whb"]//text()'))
                i_step["desc"] = lts(steps.xpath('.//div[@class="step"]/text()')).strip()
                i_step["points"] = steps.xpath('.//li//text()')
                step_num = lts(steps.xpath('.//div[@class="step_num"]//text()'))
                steps_dict[step_num] = i_step
            i_section["steps"] = steps_dict
            section_num = lts(sections.xpath('.//h3/div/span/text()'))
            sections_dict[section_num] = i_section


        ####################################################
        #The metadata which contains all the above in a presentable format
        i_meta = meta.copy()
        # i_meta["expert_review"] = i_expert_review
        i_meta["stats"] = i_stats
        # i_meta["quick_summary_section"] = i_quick_summary_section
        # i_meta["sections"] = sections_dict
        # i_meta["tip_section"] = i_tip_section
        # i_meta["warning_section"] =  i_warning_section
        # i_meta["thingsyoullneed_section"] = i_thingsyoullneed_section
        # i_meta["qa_section"] = i_qa_section
        # i_meta["video_section"] = i_video_section
        # i_meta["related_section"] = i_related_section
        # i_meta["cite_section"] = i_cite_section
        # i_meta["info_section"] = i_info_section


        kk["meta"] = i_meta
        print('\t', kk["name"])

    #Incase you want to periodically save the data, uncomment this.       
    with open('scraped_data.json', 'w') as f:
        import re
        output = json.dumps(data_root, indent=4)
        f.write(re.sub(r'(?<=\d),\s+', ', ', output))



recurse(data_root)

with open('scraped_data.json', 'w') as f:
    import re
    output = json.dumps(data_root, indent=4)
    f.write(re.sub(r'(?<=\d),\s+', ', ', output))
