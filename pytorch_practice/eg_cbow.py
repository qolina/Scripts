import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

Context_size = 2

raw_text = """We are about to study the idea of a computational process.
Computational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.""".split()

vocab = set(raw_text)
vocab_size = len(vocab)

word_to_ix = {word:i for i, word in enumerate(vocab)}
data = []
for i in range(2, len(raw_text)-2):
	context = [raw_text[i-2], raw_text[i-1], raw_text[i+1], raw_text[i+2]]
	target = raw_text[i]
	data.append((context, target))
print data[:3]

Embedding_dim = 10

class CBOW(nn.Module):
	def __init__(self, vocab_size, embedding_dim, context_size):
		super(CBOW, self).__init__()
		self.embeddings = nn.Embedding(vocab_size, embedding_dim)

		self.linear1 = nn.Linear(2*context_size*embedding_dim, 128)
		#self.linear2 = nn.Linear(128, vocab_size)

	def forward(self, inputs):
		embeds = self.embeddings(inputs).view((1, -1))
		out = self.linear1(embeds)
		log_probs = F.log_softmax(out)
		return log_probs

def make_context_vector(context, word_to_ix):
	idxs = [word_to_ix[w] for w in context]
	tensor = torch.LongTensor(idxs)
	return autograd.Variable(tensor)

losses = []
loss_function = nn.NLLLoss()
model = CBOW(len(vocab), Embedding_dim, Context_size)
optimizer = optim.SGD(model.parameters(), lr=0.001)

for epoch in range(10):
	total_loss = torch.Tensor([0])
	for context, target in data:
		context_idxs = [word_to_ix[w] for w in context]
		context_var = autograd.Variable(torch.LongTensor(context_idxs))

		model.zero_grad()

		log_probs = model(context_var)
		loss = loss_function(log_probs, autograd.Variable(
			torch.LongTensor([word_to_ix[target]])))

		loss.backward()
		optimizer.step()

		total_loss += loss.data
	losses.append(total_loss)
print losses
