from blog.models import Post, Votes, CustomUser
from django.db.models import Q, Count, F, Case, When, IntegerField


class VotingService:
    """Serviço para gerenciar o sistema de votação de posts."""
    
    @staticmethod
    def get_user_vote(post: Post, user: CustomUser) -> 'Votes | None':
        """
        Obtém o voto do usuário para um post específico.
        
        Args:
            post: O post
            user: O usuário
            
        Returns:
            O objeto Votes se existir, None caso contrário
        """
        try:
            return Votes.objects.get(origin_post=post, user_id=user)
        except Votes.DoesNotExist:
            return None
    
    @staticmethod
    def add_or_update_vote(post: Post, user: CustomUser, vote_value: bool) -> tuple[bool, str]:
        """
        Adiciona ou atualiza o voto de um usuário em um post.
        
        Args:
            post: O post
            user: O usuário
            vote_value: True para upvote, False para downvote
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            existing_vote = VotingService.get_user_vote(post, user)
            
            if existing_vote is not None:
                # Se o voto é igual ao existente, remove o voto
                if existing_vote.vote_value == vote_value:
                    VotingService.remove_vote(post, user)
                    return True, "Voto removido"
                # Se é diferente, atualiza o voto
                else:
                    old_value = existing_vote.vote_value
                    existing_vote.vote_value = vote_value
                    existing_vote.save()
                    VotingService._update_post_status(post, old_value, vote_value)
                    return True, "Voto atualizado"
            else:
                # Cria um novo voto
                Votes.objects.create(
                    origin_post=post,
                    user_id=user,
                    vote_value=vote_value
                )
                VotingService._update_post_status_new(post, vote_value)
                return True, "Voto registrado"
                
        except Exception as e:
            return False, f"Erro ao registrar voto: {str(e)}"
    
    @staticmethod
    def remove_vote(post: Post, user: CustomUser) -> bool:
        """
        Remove o voto de um usuário em um post.
        
        Args:
            post: O post
            user: O usuário
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            vote = VotingService.get_user_vote(post, user)
            if vote:
                vote_value = vote.vote_value
                vote.delete()
                VotingService._update_post_status_remove(post, vote_value)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def calculate_post_status(post: Post) -> int:
        """
        Calcula o status de um post baseado no número de votos.
        Upvotes = +1, Downvotes = -1
        
        Args:
            post: O post
            
        Returns:
            O score total do post
        """
        upvotes = Votes.objects.filter(origin_post=post, vote_value=True).count()
        downvotes = Votes.objects.filter(origin_post=post, vote_value=False).count()
        return upvotes - downvotes
    
    @staticmethod
    def _update_post_status(post: Post, old_value: bool, new_value: bool) -> None:
        """
        Atualiza o status do post ao trocar um voto.
        
        Args:
            post: O post
            old_value: Valor anterior do voto
            new_value: Novo valor do voto
        """
        if old_value == new_value:
            return
        
        adjustment = 0
        if old_value and not new_value:  # De upvote para downvote
            adjustment = -2
        elif not old_value and new_value:  # De downvote para upvote
            adjustment = 2
        
        post._status = post._status + adjustment
        post.save()
    
    @staticmethod
    def _update_post_status_new(post: Post, vote_value: bool) -> None:
        """
        Atualiza o status ao adicionar um novo voto.
        
        Args:
            post: O post
            vote_value: True para upvote, False para downvote
        """
        adjustment = 1 if vote_value else -1
        post._status = post._status + adjustment
        post.save()
    
    @staticmethod
    def _update_post_status_remove(post: Post, vote_value: bool) -> None:
        """
        Atualiza o status ao remover um voto.
        
        Args:
            post: O post
            vote_value: True se era upvote, False se era downvote
        """
        adjustment = -1 if vote_value else 1
        post._status = post._status + adjustment
        post.save()
