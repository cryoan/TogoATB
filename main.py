import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# Arbre décisionnel simplifié
decision_tree = {
    "question": "Quel est le type d'infection suspectée ?",
    "key": "type_infection",
    "options": [
        {
            "value": "colonisation",
            "recommendation": "Pas d'antibiothérapie sauf situations spécifiques (grossesse, neutropénie, geste urologique).",
            "references": ["p.25"]
        },
        {
            "value": "cystite_aigue",
            "next": {
                "question": "La patiente est-elle enceinte ?",
                "key": "grossesse",
                "options": [
                    {
                        "value": "oui",
                        "recommendation": "Fosfomycine 3g dose unique ou Pivmecillinam 400 mg 2x/j pendant 5 jours",
                        "references": ["p.26"]
                    },
                    {
                        "value": "non",
                        "next": {
                            "question": "Y a-t-il un risque de complication ?",
                            "key": "risque_complication",
                            "options": [
                                {
                                    "value": "oui",
                                    "recommendation": "Nitrofurantoïne 100 mg 2x/j pendant 5 jours ou Pivmecillinam",
                                    "references": ["p.26"]
                                },
                                {
                                    "value": "non",
                                    "recommendation": "Fosfomycine 3g dose unique",
                                    "references": ["p.26"]
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "value": "cystite_recidivante",
            "next": {
                "question": "Est-ce un épisode isolé ou répété (>4/an) ?",
                "key": "recurrence",
                "options": [
                    {
                        "value": "isolé",
                        "recommendation": "Traiter comme une cystite simple avec ECBU",
                        "references": ["p.27"]
                    },
                    {
                        "value": "répété",
                        "next": {
                            "question": "Prophylaxie nécessaire ?",
                            "key": "prophylaxie",
                            "options": [
                                {
                                    "value": "oui",
                                    "recommendation": "Fosfomycine 3g tous les 10 jours ou Nitrofurantoïne 50 mg/j",
                                    "references": ["p.27"]
                                },
                                {
                                    "value": "non",
                                    "recommendation": "Traitement ciblé après ECBU à chaque épisode",
                                    "references": ["p.27"]
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "value": "pyelonephrite_aigue",
            "next": {
                "question": "Signes de gravité ?",
                "key": "gravite",
                "options": [
                    {
                        "value": "oui",
                        "recommendation": "Ceftriaxone 1-2g/j IV ou Ciprofloxacine IV",
                        "references": ["p.28"]
                    },
                    {
                        "value": "non",
                        "next": {
                            "question": "Risque de complication ?",
                            "key": "risque_complication",
                            "options": [
                                {
                                    "value": "oui",
                                    "recommendation": "Ciprofloxacine PO 500 mg 2x/j pendant 7 jours",
                                    "references": ["p.28"]
                                },
                                {
                                    "value": "non",
                                    "recommendation": "Ciprofloxacine PO 500 mg 2x/j pendant 5 jours",
                                    "references": ["p.28"]
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "value": "infection_urinaire_masculine",
            "next": {
                "question": "Signes de rétention ou prostatite ?",
                "key": "rétention",
                "options": [
                    {
                        "value": "oui",
                        "recommendation": "Hospitalisation + Ceftriaxone IV ou Ciprofloxacine IV",
                        "references": ["p.29"]
                    },
                    {
                        "value": "non",
                        "recommendation": "Ciprofloxacine 500 mg 2x/j pendant 10-14 jours",
                        "references": ["p.29"]
                    }
                ]
            }
        }
    ]
}


def build_tree_structure(node, parent_id="root", node_id=0, tree_data=None, level=0, x_offset=0, branch_width=8):
    """Construit la structure de l'arbre pour la visualisation avec espacement optimisé"""
    if tree_data is None:
        tree_data = {"nodes": [], "edges": []}

    # Calculer le nombre total d'options pour cet embranchement
    total_options = len(node["options"])

    # Ajouter le nœud actuel (question)
    current_node_id = f"node_{node_id}"
    tree_data["nodes"].append({
        "id": current_node_id,
        "label": node["question"],
        "type": "question",
        "level": level,
        "x": x_offset,
        "y": -level * 3  # Espacement vertical plus important
    })

    # Si ce n'est pas le nœud racine, ajouter l'arête
    if parent_id != "root":
        tree_data["edges"].append({
            "source": parent_id,
            "target": current_node_id
        })

    child_node_id = node_id + 1

    # Calculer l'espacement horizontal pour les options
    option_spacing = branch_width / \
        max(1, total_options - 1) if total_options > 1 else 0
    start_x = x_offset - (branch_width / 2)

    # Traiter chaque option
    for i, option in enumerate(node["options"]):
        option_x = start_x + \
            (i * option_spacing) if total_options > 1 else x_offset
        option_node_id = f"option_{child_node_id}"

        # Ajouter le nœud d'option
        tree_data["nodes"].append({
            "id": option_node_id,
            "label": option["value"],
            "type": "option",
            "level": level + 0.5,
            "x": option_x,
            "y": -(level + 0.5) * 3
        })

        # Arête du nœud question vers l'option
        tree_data["edges"].append({
            "source": current_node_id,
            "target": option_node_id
        })

        child_node_id += 1

        if "recommendation" in option:
            # Nœud feuille (recommandation)
            rec_node_id = f"rec_{child_node_id}"
            # Raccourcir le texte de recommandation pour éviter les débordements
            short_rec = option['recommendation'][:40] + "..." if len(
                option['recommendation']) > 40 else option['recommendation']

            tree_data["nodes"].append({
                "id": rec_node_id,
                "label": short_rec,
                "type": "recommendation",
                "level": level + 1.5,
                "x": option_x,
                "y": -(level + 1.5) * 3,
                "full_recommendation": option['recommendation'],
                "references": option.get('references', [])
            })

            tree_data["edges"].append({
                "source": option_node_id,
                "target": rec_node_id
            })

            child_node_id += 1

        elif "next" in option:
            # Nœud suivant - ajuster la largeur de branche pour les sous-arbres
            # Réduire la largeur pour les niveaux inférieurs
            sub_branch_width = branch_width * 0.6
            child_node_id = build_tree_structure(
                option["next"], option_node_id, child_node_id, tree_data,
                level + 1.5, option_x, sub_branch_width
            )

    return child_node_id


def format_text_with_linebreaks(text, max_chars_per_line=25, max_lines=3):
    """Formate le texte avec des retours à la ligne pour améliorer la lisibilité"""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Si ajouter ce mot dépasse la limite de caractères
        if len(current_line + " " + word) > max_chars_per_line and current_line:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word

    # Ajouter la dernière ligne
    if current_line:
        lines.append(current_line)

    # Limiter le nombre de lignes et ajouter "..." si nécessaire
    if len(lines) > max_lines:
        lines = lines[:max_lines-1]
        lines.append(lines[-1][:max_chars_per_line-3] + "...")

    return "<br>".join(lines)


def is_node_in_path(node, user_path):
    """Vérifie si un nœud est exactement dans le chemin utilisateur avec précision stricte"""
    if not user_path:
        return False

    for step in user_path:
        # Correspondance pour les questions - doit être exacte ou très proche
        if node["type"] == "question":
            # Normalisation et comparaison stricte
            node_text = node["label"].lower().strip()
            step_text = step["question"].lower().strip()

            # Correspondance exacte d'abord
            if node_text == step_text:
                return True

            # Puis correspondance par mots-clés uniques et spécifiques
            if "gravité" in node_text and "gravité" in step_text:
                return True
            elif "complication" in node_text and "complication" in step_text:
                return True
            elif "enceinte" in node_text and "enceinte" in step_text:
                return True
            elif "récurrence" in node_text and "récurrence" in step_text:
                return True
            elif "prophylaxie" in node_text and "prophylaxie" in step_text:
                return True
            elif "rétention" in node_text and "rétention" in step_text:
                return True

        # Correspondance pour les options - doit être exactement la même
        elif node["type"] == "option":
            if step["answer"].lower().strip() == node["label"].lower().strip():
                return True

    return False


def is_final_recommendation(node, user_path):
    """Vérifie si ce nœud est LA recommandation finale unique correspondant au chemin complet"""
    if not user_path or node["type"] != "recommendation":
        return False

    # Ne marquer qu'UNE SEULE recommandation comme finale
    # C'est celle qui correspond au dernier niveau du chemin utilisateur

    # Pour l'instant, marquer seulement s'il y a un chemin complet
    # et que c'est une recommandation (on assumera qu'il n'y en a qu'une visible à la fin)
    # Cette logique sera affinée selon l'arbre réel affiché
    # Au moins 2 étapes dans le chemin pour avoir une recommandation finale
    return len(user_path) >= 2


def create_decision_tree_visualization(tree_data, user_path=None):
    """Crée la visualisation de l'arbre décisionnel avec Plotly"""

    # Séparer les nœuds par type pour un affichage différencié
    question_nodes = [n for n in tree_data["nodes"] if n["type"] == "question"]
    option_nodes = [n for n in tree_data["nodes"] if n["type"] == "option"]
    recommendation_nodes = [
        n for n in tree_data["nodes"] if n["type"] == "recommendation"]

    # Trace pour les questions (avec disques bleus, texte noir)
    question_trace = go.Scatter(
        x=[n["x"] for n in question_nodes],
        y=[n["y"] for n in question_nodes],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        textposition="middle center",
        textfont=dict(
            size=[13 if user_path and is_node_in_path(
                n, user_path) else 11 for n in question_nodes],
            color="black",  # Texte noir pour tous
            family="Arial Black"
        ),
        marker=dict(
            size=[120 if user_path and is_node_in_path(
                n, user_path) else 95 for n in question_nodes],
            color=["#1E5091" if user_path and is_node_in_path(
                n, user_path) else "#4472C4" for n in question_nodes],
            line=dict(
                width=[3 if user_path and is_node_in_path(
                    n, user_path) else 1 for n in question_nodes],
                color=["#00AA00" if user_path and is_node_in_path(
                    n, user_path) else "darkgray" for n in question_nodes]  # Vert pour le chemin
            )
        ),
        name="Questions",
        showlegend=False
    )

    # Trace pour les options (texte noir, souligné en vert si dans le chemin)
    option_trace = go.Scatter(
        x=[n["x"] for n in option_nodes],
        y=[n["y"] for n in option_nodes],
        text=[],
        mode='text',
        hoverinfo='text',
        textposition="middle center",
        textfont=dict(
            size=[15 if user_path and is_node_in_path(
                n, user_path) else 12 for n in option_nodes],
            color="black",  # Texte noir pour tous
            family="Arial Black"
        ),
        name="Options",
        showlegend=False
    )

    # Trace pour les recommandations (texte noir, contour vert pour la finale)
    recommendation_trace = go.Scatter(
        x=[n["x"] for n in recommendation_nodes],
        y=[n["y"] for n in recommendation_nodes],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        textposition="middle center",
        textfont=dict(
            size=[9 if user_path and is_final_recommendation(
                n, user_path) else 8 for n in recommendation_nodes],
            color="black"  # Texte noir pour tous
        ),
        marker=dict(
            size=[85 if user_path and is_final_recommendation(
                n, user_path) else 65 for n in recommendation_nodes],
            color=["#FFD700" if user_path and is_final_recommendation(
                n, user_path) else "#FF8C00" for n in recommendation_nodes],
            line=dict(
                width=[4 if user_path and is_final_recommendation(
                    n, user_path) else 1 for n in recommendation_nodes],
                color=["#00AA00" if user_path and is_final_recommendation(
                    n, user_path) else "darkgray" for n in recommendation_nodes]  # Vert pour la finale
            ),
            symbol="square"
        ),
        name="Recommandations",
        showlegend=False
    )

    # Ajouter le texte formaté pour chaque type de nœud
    for node in question_nodes:
        display_text = format_text_with_linebreaks(
            node["label"], max_chars_per_line=30, max_lines=3)
        question_trace['text'] += (display_text,)

    for node in option_nodes:
        # Pour les options, ajouter un soulignement vert si dans le chemin
        display_text = format_text_with_linebreaks(
            node["label"], max_chars_per_line=20, max_lines=2)
        if user_path and is_node_in_path(node, user_path):
            # Utiliser des balises HTML pour souligner en vert
            display_text = f'<span style="text-decoration: underline; text-decoration-color: #00AA00; text-decoration-thickness: 3px;">{display_text}</span>'
        option_trace['text'] += (display_text,)

    for node in recommendation_nodes:
        # Pour les recommandations, utiliser un formatage plus compact
        display_text = format_text_with_linebreaks(
            node["label"], max_chars_per_line=20, max_lines=4)
        recommendation_trace['text'] += (display_text,)

    # Créer les arêtes (vert pour le chemin choisi)
    edge_trace = []
    for edge in tree_data["edges"]:
        source_node = next(
            n for n in tree_data["nodes"] if n["id"] == edge["source"])
        target_node = next(
            n for n in tree_data["nodes"] if n["id"] == edge["target"])

        # Déterminer la couleur de l'arête (vert si dans le chemin utilisateur)
        edge_color = "#00AA00" if user_path and is_edge_in_path(
            edge, user_path, tree_data) else "#CCCCCC"
        edge_width = 5 if edge_color == "#00AA00" else 2

        edge_trace.append(go.Scatter(
            x=[source_node["x"], target_node["x"], None],
            y=[source_node["y"], target_node["y"], None],
            mode='lines',
            line=dict(width=edge_width, color=edge_color),
            showlegend=False,
            hoverinfo='none'
        ))

    # Créer la figure avec des dimensions optimisées
    fig = go.Figure(data=edge_trace + [question_trace, option_trace, recommendation_trace],
                    layout=go.Layout(
        title={
            'text': "Arbre Décisionnel - Antibiothérapie Infections Urinaires",
            'font': {'size': 18},
            'x': 0.5
        },
        showlegend=False,
        hovermode='closest',
        margin=dict(b=50, l=50, r=50, t=80),
        annotations=[
            dict(
                text="🟢 Chemin parcouru | 🔵 Questions | ⚫ Options | 🟠 Recommandations",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.05,
                xanchor="center", yanchor="top",
                font=dict(size=14)
            )
        ],
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-15, 15]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-20, 2]
        ),
        plot_bgcolor='white',
        height=800,
        width=1200
    ))

    return fig


def filter_path_for_tree(path, clinical_situation):
    """Filtre le chemin pour ne garder que les étapes pertinentes pour l'arbre filtré"""
    if not path:
        return []

    # Pour la colonisation, il n'y a qu'une étape (choix direct)
    if clinical_situation == "colonisation":
        return []  # Pas de sous-arbre à parcourir

    # Pour les autres situations, enlever la première étape (choix de situation clinique)
    # et garder les étapes suivantes qui correspondent au sous-arbre
    filtered_path = []

    # Commencer à partir de la deuxième étape (index 1)
    for i in range(1, len(path)):
        step = path[i]
        filtered_path.append({
            "question": step["question"],
            "answer": step["answer"],
            "step": len(filtered_path) + 1
        })

    return filtered_path


def is_edge_in_path(edge, user_path, tree_data):
    """Vérifie si une arête fait partie du chemin exact de l'utilisateur"""
    if not user_path:
        return False

    source_node = next(
        n for n in tree_data["nodes"] if n["id"] == edge["source"])
    target_node = next(
        n for n in tree_data["nodes"] if n["id"] == edge["target"])

    # Une arête est dans le chemin SEULEMENT si :
    # 1. Le nœud source est une question dans le chemin ET le nœud target est l'option correspondante
    # 2. OU le nœud source est une option dans le chemin ET le nœud target est la question suivante
    # 3. OU le nœud source est une option dans le chemin ET le nœud target est la recommandation finale

    source_in_path = is_node_in_path(source_node, user_path)
    target_in_path = is_node_in_path(target_node, user_path)
    target_is_final_rec = is_final_recommendation(target_node, user_path)

    # Être très restrictif : les deux nœuds doivent être dans le chemin
    # OU c'est une connexion vers la recommandation finale
    return (source_in_path and target_in_path) or (source_in_path and target_is_final_rec)


def extract_clinical_situation_tree(decision_tree, clinical_situation):
    """Extrait la partie de l'arbre correspondant à la situation clinique choisie"""

    # Trouver l'option correspondant à la situation clinique
    selected_option = None
    for option in decision_tree["options"]:
        if option["value"] == clinical_situation:
            selected_option = option
            break

    if not selected_option:
        return decision_tree  # Retourner l'arbre complet si non trouvé

    # Si l'option a une recommandation directe, créer un arbre simple
    if "recommendation" in selected_option:
        return {
            "question": f"Situation: {clinical_situation}",
            "key": "situation",
            "options": [selected_option]
        }

    # Si l'option a un sous-arbre, le retourner
    elif "next" in selected_option:
        return selected_option["next"]

    return decision_tree


def display_node(node, answers, path):
    st.markdown(f"**{node['question']}**")
    options = [opt["value"] for opt in node["options"]]
    choice = st.radio("Sélectionnez une option :", options, key=node["key"])
    selected = next(opt for opt in node["options"] if opt["value"] == choice)
    answers[node["key"]] = choice
    path.append({
        "question": node['question'],
        "answer": choice,
        "step": len(path) + 1
    })

    if "recommendation" in selected:
        st.success(f"Recommandation : {selected['recommendation']}")
        st.markdown(f"🔖 Références : {', '.join(selected['references'])}")

        # Déterminer la situation clinique (premier choix)
        clinical_situation = path[0]['answer'] if path else None

        # Affichage de l'arbre décisionnel filtré avec chemin parcouru
        st.markdown("---")
        st.markdown(f"### 🌳 Arbre Décisionnel - {clinical_situation}")

        # Extraire et construire la structure de l'arbre pour la situation clinique
        filtered_tree = extract_clinical_situation_tree(
            decision_tree, clinical_situation)
        tree_data = {"nodes": [], "edges": []}
        build_tree_structure(
            filtered_tree, tree_data=tree_data, branch_width=10)

        # Filtrer le chemin pour correspondre à l'arbre filtré
        filtered_path = filter_path_for_tree(path, clinical_situation)

        # Debug: afficher le chemin filtré
        if filtered_path:
            st.write("**Debug - Chemin filtré utilisé pour l'arbre:**")
            for step in filtered_path:
                st.write(f"- {step['question']} → {step['answer']}")
        else:
            st.write("**Debug - Aucun chemin filtré (situation directe)**")

        # Créer et afficher la visualisation avec le chemin filtré
        fig = create_decision_tree_visualization(tree_data, filtered_path)
        st.plotly_chart(fig, use_container_width=True)

        # Affichage du chemin décisionnel textuel complet
        st.markdown("### 🗺️ Chemin décisionnel parcouru")
        for i, step in enumerate(path, 1):
            st.markdown(f"**Étape {i}:** {step['question']}")
            st.markdown(f"➜ *Réponse:* **{step['answer']}**")
            if i < len(path):
                st.markdown("⬇️")

        st.info(
            f"**Situation clinique identifiée:** {path[0]['answer'] if path else 'Non définie'}")

    elif "next" in selected:
        display_node(selected["next"], answers, path)


def main():
    st.set_page_config(page_title="Assistant Antibiothérapie", page_icon="💊")
    st.title("💊 Assistant Antibiothérapie – Infections Urinaires")
    st.write("Répondez aux questions pour obtenir une recommandation thérapeutique.")

    answers = {}
    path = []
    display_node(decision_tree, answers, path)


if __name__ == "__main__":
    main()
