from tgtoken import TOKEN
import telebot
import networkx as nx
import io
import matplotlib.pyplot as plt
import gensim
import logging
import pandas as pd
import urllib.request
from gensim.models import word2vec

model = gensim.models.Word2Vec.load("model.model")
srn = []
datasr = pd.read_csv('surnames.csv')
for i in range(len(datasr)):
    srn.append(datasr.loc[i, 'surnames'])


def visualize_graph(graph_dict, edge_labels, surname):
    G = nx.Graph()
    for node, neighbors in graph_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=12,
            font_weight='bold', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green', font_size=10,
                                 font_family='sans-serif', rotate=False)
    nx.draw_networkx_nodes(G, pos, nodelist=[surname], node_color='salmon', node_size=4000)
    plt.title("Граф связей личностей", fontsize=20)
    pic = io.BytesIO()
    plt.savefig(pic, format='png')
    pic.seek(0)
    plt.close()
    return pic


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    msg = str(message.text).lower()
    if msg in model.wv.key_to_index:
        if msg in srn:
            try:
                dcpr = {}
                dcprv = {}
                rec = []

                def prd(prs):
                    rec.append(prs.title())
                    sim = model.wv.most_similar(prs.lower(), topn=10)
                    psim = []
                    dcpr[prs.title()] = []
                    for i in sim:
                        if i[0] in srn:
                            psim.append((i[0].title(), i[1]))
                    for i in range(len(psim)):
                        if i <= 2:
                            dcpr[prs.title()].append(psim[i][0].title())
                            dcprv[(prs.title(), psim[i][0].title())] = round(psim[i][1], 2)
                            if psim[i][0].title() not in rec and len(rec) < 10:
                                prd(psim[i][0].title())
                        else:
                            break
                    return

                prd(msg)
                bot.send_photo(chat_id=message.chat.id, photo=visualize_graph(dcpr, dcprv, msg.title()))
            except:
                bot.send_message(message.chat.id, "Ошибка, попробуйте снова")
        else:
            bot.send_message(message.chat.id, "Это не личность")
    else:
        bot.send_message(message.chat.id, "Слово не найдено")


if __name__ == '__main__':
    plt.switch_backend('Agg')
    bot.infinity_polling()